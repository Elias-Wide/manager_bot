from sqladmin import ModelView

from app.core.constants import ADMIN_VIEW_PAGE_SIZE
from app.offices.models import Offices
from app.regions.models import Regions
from app.reports.models import Reports
from app.users.models import Users, WorkDays


class UsersAdmin(ModelView, model=Users):
    """
    Admin page settings for the Users model.

    Configures the display, search, and sorting options for users in the admin panel.
    """

    page_size = ADMIN_VIEW_PAGE_SIZE
    column_list = [
        Users.id,
        Users.username,
        Users.telegram_id,
        Users.office_id,
        Users.phone_number,
        Users.ban,
    ] + [Users.offices]
    name = "Пользователь"
    name_plural = "Пользователи"
    can_delete = True
    column_sortable_list = [Users.office_id]
    column_searchable_list = [
        Users.username,
        Users.telegram_id,
        Users.office_id,
        Users.first_name,
        Users.last_name,
    ]
    icon = "fa-solid fa-user"


class OfficesAdmin(ModelView, model=Offices):
    """
    Admin page settings for the Offices model.

    Configures the display, search, and sorting options for offices in the admin panel.
    """

    column_list = [c.name for c in Offices.__table__.c] + [
        Offices.region,
        Offices.managers,
    ]
    name = "Офис"
    name_plural = "Офисы"
    can_delete = True
    column_sortable_list = [Offices.addres, Offices.region_id]
    column_searchable_list = [Offices.addres, Offices.id]
    icon = "fa fa-house"


class RegionsAdmin(ModelView, model=Regions):
    """
    Admin page settings for the Regions model.

    Configures the display, search, and sorting options for regions in the admin panel.
    """

    column_list = [c.name for c in Regions.__table__.c] + [
        Regions.admins,
        Regions.offices,
    ]
    name = "Регион"
    name_plural = "Регионы"
    can_delete = True
    column_sortable_list = [Regions.name]
    column_searchable_list = [Regions.name]
    icon = "fa fa-map"


class ReportsAdmin(ModelView, model=Reports):
    """
    Admin page settings for the Reports model.

    Configures the display, search, and sorting options for reports in the admin panel.
    """

    column_list = [Reports.id, Reports.office_id, Reports.created_at]
    name = "Отчет прихода"
    name_plural = "Отчеты прихода"
    can_delete = True
    column_sortable_list = [Reports.created_at]
    column_searchable_list = [Reports.office_id]
    icon = "fa fa-file"


class WorkDaysAdmin(ModelView, model=WorkDays):
    """
    Admin page settings for the WorkDays model.

    Configures the display, search, and sorting options for workdays in the admin panel.
    """

    column_list = [WorkDays.id, WorkDays.day, WorkDays.user]
    name = "Дни рабочие"
    name_plural = "График работы"
    can_delete = True
    column_sortable_list = [WorkDays.user]
    column_searchable_list = [WorkDays.user, WorkDays.day]
    icon = "fa fa-file"


admin_views: tuple[ModelView] = (
    UsersAdmin,
    OfficesAdmin,
    RegionsAdmin,
    ReportsAdmin,
    WorkDaysAdmin,
)
