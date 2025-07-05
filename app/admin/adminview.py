from sqladmin import ModelView
from app.core.constants import ADMIN_VIEW_PAGE_SIZE
from app.points.models import Points
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
        Users.point_id,
        Users.phone_number,
        Users.ban,
        Users.is_region_admin,
    ] + [Users.points]
    name = "Пользователь"
    name_plural = "Пользователи"
    can_delete = True
    column_sortable_list = [Users.is_region_admin]
    column_searchable_list = [
        Users.username,
        Users.telegram_id,
        Users.point_id,
        Users.first_name,
        Users.last_name,
    ]
    icon = "fa-solid fa-user"


class PointsAdmin(ModelView, model=Points):
    """Настройки страницы офисов."""

    column_list = [c.name for c in Points.__table__.c] + [
        Points.region,
        Points.managers,
    ]
    name = "Офис"
    name_plural = "Офисы"
    can_delete = True
    column_sortable_list = [Points.addres, Points.region_id]
    column_searchable_list = [Points.addres, Points.id]
    icon = "fa fa-house"


class RegionsAdmin(ModelView, model=Regions):
    """Настройки страницы офисов."""

    column_list = [c.name for c in Regions.__table__.c] + [
        Regions.ceo,
        Regions.points,
    ]
    name = "Регион"
    name_plural = "Регионы"
    can_delete = True
    column_sortable_list = [Regions.name]
    column_searchable_list = [Regions.name, Regions.ceo]
    icon = "fa fa-map"


class ReportsAdmin(ModelView, model=Reports):
    """Report admin page settings."""

    column_list = [Reports.id, Reports.point_id, Reports.created_at]
    name = "Отчет прихода"
    name_plural = "Отчеты прихода"
    can_delete = True
    column_sortable_list = [Reports.created_at]
    column_searchable_list = [Reports.point_id]
    icon = "fa fa-file"


admin_views: tuple[ModelView] = (
    UsersAdmin,
    PointsAdmin,
    RegionsAdmin,
    ReportsAdmin,
)
