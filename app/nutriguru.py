from sqlalchemy.orm import Session
from sqlalchemy import create_engine, select
from EdgeGPT import Chatbot, ConversationStyle
import asyncio
import json
from pprint import pprint
from loguru import logger
import sys
from .utils import create_db_connection, json_to_products_list
from .models import Product, Manufacturer

with open('./cookies.json', 'r') as f:
    cookies = json.load(f)

manufacturer = "Garden of Life"
product_name = "Mykind Organics Plant Calcium"
product_sku = "90 vegan tabs"

prompt = f"Categorize product in a table. Use NA for not available. Specify net volume, main ingredient(s), main active ingredient, daily dose, pharmaceutical form(powder, caps, gummy bear etc.), main benefits, main side effects, retail price, category of supplements, sub-category of supplements, is organic?, is non-GMO?, is natural?, is vegan?. the manufacturer is {manufacturer} : , select_manufacturer, product code: {product_sku} product name: {product_name} ,select_product, return in json format, don't list sources or links"

products = json_to_products_list(json_file="./products.json")

engine = create_engine("sqlite:///nutriguru.db", echo=True)

# create tables if they dont exist
Manufacturer.__table__.create(bind=engine, checkfirst=True)
Product.__table__.create(bind=engine, checkfirst=True)


async def main():
    logger.add(sys.stdout, colorize=True,
               format="<green>{time}</green> <level>{message}</level>")
    logger.add("log.log")

    logger.info("new session created")

    for product in products:

        product_sku = product.get("id")
        product_name = product.get("product_name")
        product_manufacturer = product.get("manufacturer")

        logger.info(f"processing product: {product_sku}")

        bot = Chatbot(cookies=cookies)
        data = await bot.ask(prompt=prompt, conversation_style=ConversationStyle.precise)
        await bot.close()

        with Session(engine) as session:

            manufacturer = session.query(Manufacturer).filter_by(
                name=product_manufacturer).one_or_none()

            if not manufacturer:
                manufacturer = Manufacturer(name=product_manufacturer)
                session.add(manufacturer)
                session.commit()
                session.refresh(manufacturer)
                logger.info(
                    f"Manufacturer {manufacturer.name} not found, created in db.")

            product = session.query(Product).filter_by(
                sku=product_sku).one_or_none()

            if not product:
                product = Product(
                    sku=product_sku, name=product_name, manufacturer_id=manufacturer.id, data=data)
                session.add(product)
                session.commit()
                session.flush()
                logger.info(
                    f"Product {product.sku} | {product.name} created in db. \n\n")

if __name__ == "__main__":
    asyncio.run(main())
