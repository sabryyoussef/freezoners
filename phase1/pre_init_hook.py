import logging
from odoo.modules.module import get_module_resource

def pre_init_hook(cr):
    # Check if all required modules are installed before proceeding
    required_modules = [
        "base",
        "mail",
        "account",
        "documents",
        "sale",
        "sale_project",
        "web",
        "client_documents",
        "hr_expense",
        "project",
        "crm",
        "cabinet_directory",
    ]
    cr.execute("SELECT name, state FROM ir_module_module WHERE name IN %s", (tuple(required_modules),))
    installed = {row[0]: row[1] for row in cr.fetchall()}
    missing = [m for m in required_modules if installed.get(m) not in ("installed", "to upgrade")]
    if missing:
        logging.error(f"The following required modules are not installed: {missing}")
        raise Exception(f"Missing required modules: {', '.join(missing)}")
