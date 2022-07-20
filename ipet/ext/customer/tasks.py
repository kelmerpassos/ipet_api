"""Module that performs client package tasks."""
from logging import Logger
from flask_apscheduler import APScheduler
from pathlib import Path
from ipet.ext.libs.ssh import create_ssh_client
from ipet.ext.config import environment_var
from scp import SCPClient
import aiofiles
import asyncio
from ipet.ext.customer.models import AssocProductCustomer
from ipet.ext.customer.schemas import ProductCustomerSchema
from ipet.ext.customer.models import Customer
from ipet.ext.product.models import Product

async def read_base_offline(filename: str, logger: Logger):
    """Read validates and saves, offline database record.

    Args:
        filename (str): Offline database file name
        logger (Logger): Logger instance
    """
    async with aiofiles.open(filename, mode="r") as f:
        async for line in f:
            try:
                data = ProductCustomerSchema.normalize_data_list(line.split("|"))
            except ValueError as exp:
                logger.error(exp.args[0])
            if not AssocProductCustomer.query.filter(
                AssocProductCustomer.customer_id == data[0],
                AssocProductCustomer.product_id == data[1],
            ).first():
                customer = Customer.query.get(data[0])
                product = Product.query.get(data[1])
                if customer and product:
                    ass = AssocProductCustomer(customer=customer, product=product, created_at=data[2])
                    ass.save()
                else:
                    logger.error(f"ID not found: product_id {data[1]}, customer_id {data[0]}")
            else:
                logger.info(f"Customer already owns this product: product_id {data[1]}, customer_id {data[0]}")



def register_tasks(scheduler: APScheduler):
    """Register functions that will be executed periodically in another Thread.

    Args:
        scheduler (APScheduler): APScheduler instance
    """

    @scheduler.task(
        "interval", id="task_get_product_customer", seconds=20, misfire_grace_time=900
    )
    def task_get_product_customer():
        with scheduler.app.app_context():
            ssh = create_ssh_client(
                environment_var.SSH_HOST,
                environment_var.SSH_PORT,
                environment_var.SSH_USER,
                environment_var.SSH_PASSWORD,
            )
            filename = Path(environment_var.DB_FILE_PATH).name
            try:
                with SCPClient(ssh.get_transport()) as scp:
                    scp.get(
                        environment_var.DB_FILE_PATH,
                        filename,
                    )
                scheduler.app.logger.info("File created")
            except:
                scheduler.app.logger.exception("Error collecting file")
            finally:
                ssh.close()
            asyncio.run(read_base_offline(filename, scheduler.app.logger))
