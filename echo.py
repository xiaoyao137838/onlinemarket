# echo.py

# def echo(text: str, repetitions: int = 3) -> str:
#     """Imitate a real-world echo."""
#     echoed_text = ""
#     for i in range(repetitions, 0, -1):
#         echoed_text += f"{text[-i:]}\n"
#     return f"{echoed_text.lower()}."

# if __name__ == "__main__":
#     text = input("Yell something at a mountain: ")
#     print(echo(text))
from kafka import KafkaProducer
from kafka import KafkaConsumer
# from flashsale.models import FlashSale, FlashOrder
# from market.models import Tax
c = KafkaConsumer()
print(type(c))
# if __name__=='__main__':
#     print('hello')