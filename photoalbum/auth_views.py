from django.contrib.auth.views import LogoutView as DjangoLogoutView


class LogoutView(DjangoLogoutView):
    """Allow GET and POST so logout links work and redirect to the album list."""

    http_method_names = ['get', 'post', 'options', 'head']

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)
