from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


def environment_callback(request):
    """
    Returns a list of two values: text and color type of the label
    displayed in top right corner of the admin.
    """
    return ["Production", "danger"]


def environment_title_prefix_callback(request):
    """
    Returns a prefix string for the environment label in the title tag.
    """
    return "Env:"


def dashboard_callback(request, context):
    """
    Prepare custom variables for admin index template (dashboard).
    """
    context.update(
        {
            "sample": "example",
        }
    )
    return context


def badge_callback(request):
    """
    Return badge count or any badge value for UI.
    """
    return 3


def permission_callback(request):
    """
    Return True/False if user has the permission to see certain items.
    """
    return request.user.has_perm("sample_app.change_model")


UNFOLD = {
    "SITE_TITLE": "News Portal",
    "SITE_HEADER": "My Admin Dashboard",
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",
            "title": _("My site"),
            "link": "https://example.com",
        },
    ],
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("users/news.jpg"),
        "dark": lambda request: static("users/news.jpg"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("users/news.jpg"),
        "dark": lambda request: static("users/news.jpg"),
    },
    "SITE_LOGO_SMALL": "users/news.jpg",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("users/news.jpg.png"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,
    "ENVIRONMENT": environment_callback,
    "ENVIRONMENT_TITLE_PREFIX": environment_title_prefix_callback,
    "DASHBOARD_CALLBACK": dashboard_callback,
    "THEME": "dark",
    "LOGIN": {
        "image": lambda request: static("sample/login-bg.jpg"),
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },
    "LOGOUT": {
        "redirect_after": lambda request: reverse_lazy("admin:index"),
    },
    "STYLES": [
        lambda request: static("css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("js/script.js"),
    ],
    "BORDER_RADIUS": "6px",
    "COLORS": {
        "base": {
            "50": "249, 250, 251",
            "100": "243, 244, 246",
            "200": "229, 231, 235",
            "300": "209, 213, 219",
            "400": "156, 163, 175",
            "500": "107, 114, 128",
            "600": "75, 85, 99",
            "700": "55, 65, 81",
            "800": "31, 41, 55",
            "900": "17, 24, 39",
            "950": "3, 7, 18",
        },
        "primary": {
            "50": "250, 245, 255",
            "100": "243, 232, 255",
            "200": "233, 213, 255",
            "300": "216, 180, 254",
            "400": "192, 132, 252",
            "500": "168, 85, 247",
            "600": "147, 51, 234",
            "700": "126, 34, 206",
            "800": "107, 33, 168",
            "900": "88, 28, 135",
            "950": "59, 7, 100",
        },
        "font": {
            "subtle-light": "var(--color-base-500)",
            "subtle-dark": "var(--color-base-400)",
            "default-light": "var(--color-base-600)",
            "default-dark": "var(--color-base-300)",
            "important-light": "var(--color-base-900)",
            "important-dark": "var(--color-base-100)",
        },
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "fr": "🇫🇷",
                "nl": "🇧🇪",
            },
        },
    },
    "SIDEBAR": {
        "show_search": False,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Dashboard"),
                "separator": True,
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Support"),
                        "icon": "support",
                        "link": reverse_lazy("admin:users_support_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            {
                "title": _("Auth"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_customuser_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "groups",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
            {
                "title": _("News"),
                "icon": "newspaper",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Category"),
                        "icon": "folder",
                        "link": reverse_lazy("admin:news_category_changelist"),
                    },
                    {
                        "title": _("Create News"),
                        "icon": "article",
                        "link": reverse_lazy("admin:news_newspost_changelist"),
                    },
                    {
                        "title": _("Likes"),
                        "icon": "favorite",
                        "link": reverse_lazy("admin:news_like_changelist"),
                    },
                    {
                        "title": _("Tags"),
                        "icon": "label",
                        "link": reverse_lazy("admin:news_customtag_changelist"),
                    },
                    {
                        "title": _("Comments"),
                        "icon": "message",
                        "link": reverse_lazy("admin:news_comment_changelist"),
                    },
                    {
                        "title": _("Bookmark"),
                        "icon": "bookmark",
                        "link": reverse_lazy("admin:news_bookmark_changelist"),
                    },
                    {
                        "title": _("Notifications"),
                        "icon": "notifications",
                        "link": reverse_lazy(
                            "admin:notifications_notification_changelist"
                        ),
                    },
                ],
            },
            {
                "title": _("Stocks"),
                "icon": "bar_chart",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Sector"),
                        "icon": "business",
                        "link": reverse_lazy("admin:scraper_sector_changelist"),
                    },
                    {
                        "title": _("Symbol"),
                        "icon": "emoji_symbols",
                        "link": reverse_lazy("admin:scraper_symbol_changelist"),
                    },
                    {
                        "title": _("Keyword"),
                        "icon": "label",
                        "link": reverse_lazy("admin:scraper_keyword_changelist"),
                    },
                    {
                        "title": _("StockNews URL"),
                        "icon": "link",
                        "link": reverse_lazy("admin:scraper_stocknewsurl_changelist"),
                    },
                    {
                        "title": _("StockNews URL Rule"),
                        "icon": "rule",
                        "link": reverse_lazy(
                            "admin:scraper_stocknewsurlrule_changelist"
                        ),
                    },
                    {
                        "title": _("News URL"),
                        "icon": "link",
                        "link": reverse_lazy("admin:scraper_newsurl_changelist"),
                    },
                    {
                        "title": _("News URL Rule"),
                        "icon": "rule",
                        "link": reverse_lazy("admin:scraper_newsurlrule_changelist"),
                    },
                    {
                        "title": _("Stock Record"),
                        "icon": "assessment",
                        "link": reverse_lazy("admin:scraper_stockrecord_changelist"),
                    },
                    {
                        "title": _("Announcement"),
                        "icon": "announcement",
                        "link": reverse_lazy("admin:scraper_announcement_changelist"),
                    },
                ],
            },
            {
                "title": _("Celery"),
                "icon": "schedule",
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Periodic Tasks"),
                        "icon": "event_repeat",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_periodictask_changelist"
                        ),
                    },
                    {
                        "title": _("Crontabs"),
                        "icon": "schedule",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_crontabschedule_changelist"
                        ),
                    },
                    {
                        "title": _("Intervals"),
                        "icon": "timer",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_intervalschedule_changelist"
                        ),
                    },
                    {
                        "title": _("Clocked Tasks"),
                        "icon": "alarm",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_clockedschedule_changelist"
                        ),
                    },
                    {
                        "title": _("Solar Schedules"),
                        "icon": "sunny",
                        "link": reverse_lazy(
                            "admin:django_celery_beat_solarschedule_changelist"
                        ),
                    },
                ],
            },
        ],
    },
}
