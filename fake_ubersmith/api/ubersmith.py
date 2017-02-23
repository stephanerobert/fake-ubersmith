from flask import request

from fake_ubersmith.api.base import Base
from fake_ubersmith.api.utils.response import response


class UbersmithBase(Base):
    def __init__(self, data_store):
        super().__init__(data_store)

        self.crash_mode = False

    def hook_to(self, server):
        self.app = server
        self.app.add_url_rule(
            '/api/2.0/',
            view_func=self._route_method,
            methods=["POST"]
        )

        self.register_endpoints(
            ubersmith_method='hidden.enable_crash_mode',
            function=self.enable_crash_mode
        )
        self.register_endpoints(
            ubersmith_method='hidden.disable_crash_mode',
            function=self.disable_crash_mode
        )

    def enable_crash_mode(self, form_data):
        self.crash_mode = True
        return response(data="Crash Mode Enabled")

    def disable_crash_mode(self, form_data):
        self.crash_mode = False
        return response(data="Crash Mode Disabled")

    def register_endpoints(self, ubersmith_method, function):
        self.methods[ubersmith_method] = function

    def _should_crash(self, method):
        return method not in ['hidden.enable_crash_mode', 'hidden.disable_crash_mode'] and self.crash_mode

    def _route_method(self):
        method = request.form['method']
        if self._should_crash(method):
            raise FakeUbersmithError("Crash mode was enabled")

        return self.methods[method](request.form)


class FakeUbersmithError:
    def __init__(self, code=None, message=None):
        self.code = code
        self.message = message
