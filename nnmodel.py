
class NNModel:
  
  def __init__(self) -> None:
    self.__embs = list()  # массив с ембедингами от эталонов

  def predict(self, inp: list):
    """
    в inp - list[dict] 
      "id", "name", "props",
    """

    # your code here
    return inp

  def add_embs(self, embs: list):
    # добавление новых ембедингов в озу модели
    self.__embs += embs

  def update_refs(self, refs: list):
    # код для добавления эмбедингов в бд
    # не трогай, надо изменить
    embends = list()
    for ref in refs:
      embends.append({
        'product_id':ref['product_id'], 
        'embends': ref['name'] + ''.join(ref['props'])
        })
    return embends
