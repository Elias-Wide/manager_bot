from sqladmin import ModelView
from app.core.constants import ADMIN_VIEW_PAGE_SIZE
from app.offices.models import Offices
from app.regions.models import Regions
from app.users.models import Users
from app.reports.models import Reports


class UsersAdmin(ModelView, model=Users):
    """Настройка страницы пользователей."""

    page_size = ADMIN_VIEW_PAGE_SIZE
    column_list = [
        Users.id,
        Users.username,
        Users.telegram_id,
        Users.office_id,
        Users.phone_number,
        Users.ban,
        Users.is_region_admin,
    ] + [Users.offices]
    name = "Пользователь"
    name_plural = "Пользователи"
    can_delete = True
    column_sortable_list = [Users.is_region_admin]
    column_searchable_list = [
        Users.username,
        Users.telegram_id,
        Users.office_id,
        Users.first_name,
        Users.last_name,
    ]
    icon = "fa-solid fa-user"


class OfficesAdmin(ModelView, model=Offices):
    """Настройки страницы офисов."""

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
    """Настройки страницы офисов."""

    column_list = [c.name for c in Regions.__table__.c] + [
        Regions.ceo,
        Regions.offices,
    ]
    name = "Регион"
    name_plural = "Регионы"
    can_delete = True
    column_sortable_list = [Regions.name]
    column_searchable_list = [Regions.name, Regions.ceo]
    icon = "fa fa-map"


class ReportsAdmin(ModelView, model=Reports):
    """Report admin page settings."""

    column_list = [Reports.id, Reports.office_id, Reports.created_at]
    name = "Отчет прихода"
    name_plural = "Отчеты прихода"
    can_delete = True
    column_sortable_list = [Reports.created_at]
    column_searchable_list = [Reports.office_id]
    icon = "fa fa-file"


admin_views: tuple[ModelView] = (
    UsersAdmin,
    OfficesAdmin,
    RegionsAdmin,
    ReportsAdmin,
)
