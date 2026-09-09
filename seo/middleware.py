from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from .models import Redirect

class RedirectMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if response.status_code == 404:
            path = request.path
            redirect_obj = Redirect.objects.filter(old_path=path, is_active=True).first()
            if not redirect_obj and path.endswith('/'):
                redirect_obj = Redirect.objects.filter(old_path=path[:-1], is_active=True).first()
            elif not redirect_obj and not path.endswith('/'):
                redirect_obj = Redirect.objects.filter(old_path=f"{path}/", is_active=True).first()

            if redirect_obj:
                if redirect_obj.status_code == 301:
                    return HttpResponsePermanentRedirect(redirect_obj.new_path)
                return HttpResponseRedirect(redirect_obj.new_path)

        return response
