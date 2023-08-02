from .registration_handlers import register_registration_handlers
from .start_handlers import register_start_handlers
from .admin_handlers import register_mailing_handlers, register_main_admin_handlers, register_new_coach_handlers
from .choose_coach_handlers import register_choose_coach_handlers


def register_all_handlers(dp):
    register_registration_handlers(dp)
    register_start_handlers(dp)
    register_main_admin_handlers(dp)
    register_mailing_handlers(dp)
    register_new_coach_handlers(dp)
    register_choose_coach_handlers(dp)