from django.apps import AppConfig
from django.core.exceptions import ImproperlyConfigured
from django.urls import URLPattern, reverse_lazy

class ConfigMixin(object):
    """
    Base  app configuration mixin, used to extend :py:class:`django.apps.AppConfig`
    to also provide URL configurations and permissions.
    """
    # Instance namespace for the URLs
    namespace = None
    login_url = None

    #: A name that allows the functionality within this app to be disabled
    hidable_feature_name = None

    #: Maps view names to lists of permissions. We expect tuples of
    #: lists as dictionary values. A list is a set of permissions that all
    #: need to be fulfilled (AND). Only one set of permissions has to be
    #: fulfilled (OR).
    #: If there's only one set of permissions, as a shortcut, you can also
    #: just define one list.
    permissions_map = {}

    #: Default permission for any view not in permissions_map
    default_permissions = None

    def __init__(self, app_name, app_module, namespace=None, **kwargs):
        """
        kwargs:
            namespace: optionally specify the URL instance namespace
        """
        app_config_attrs = [
            'name',
            'module',
            'apps',
            'label',
            'verbose_name',
            'path',
            'models_module',
            'models',
        ]
        # To ensure sub classes do not add kwargs that are used by
        # :py:class:`django.apps.AppConfig`
        clashing_kwargs = set(kwargs).intersection(app_config_attrs)
        if clashing_kwargs:
            raise ImproperlyConfigured(
                "Passed in kwargs can't be named the same as properties of "
                "AppConfig; clashing: %s." % ", ".join(clashing_kwargs))
        super().__init__(app_name, app_module)
        if namespace is not None:
            self.namespace = namespace
        # Set all kwargs as object attributes
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_urls(self):
        return []

    def post_process_urls(self, urlpatterns):


        for pattern in urlpatterns:
            if hasattr(pattern, 'url_patterns'):
                self.post_process_urls(pattern.url_patterns)

            if isinstance(pattern, URLPattern):
                # Apply the custom view decorator (if any) set for this class if this
                # is a URL Pattern.
                decorator = self.get_url_decorator(pattern)
                if decorator:
                    pattern.callback = decorator(pattern.callback)

        return urlpatterns

    def get_permissions(self, url):
        # url namespaced?
        if url is not None and ':' in url:
            view_name = url.split(':')[1]
        else:
            view_name = url
        return self.permissions_map.get(view_name, self.default_permissions)

    def permissions_required(permissions, login_url=None):

        if login_url is None:
            login_url = reverse_lazy('customer:login')

    def get_url_decorator(self, pattern):
        permissions = self.get_permissions(pattern.name)
        if permissions:
            return self.permissions_required(permissions, login_url=self.login_url)

    @property
    def urls(self):
        # We set the application and instance namespace here
        return self.get_urls(), self.label, self.namespace


class Config(ConfigMixin, AppConfig):
    pass


class DashboardConfig(Config):
    login_url = reverse_lazy('dashboard:login')