from back_api import models
import pickle


class Singletone(type):
  _instances = {}
  def __call__(cls, *args, **kwargs):
    if cls not in cls._instances:
      cls._instances[cls] = super(Singletone, cls).__call__(*args, **kwargs)
    return cls._instances[cls]


class Serializer:
  pass

class JsonSer(Serializer):
  
  def __init__(self) -> None:
    pass
  
  def prepare(self, items):
    return items

  def mp_concat(self, prods: list, refs: list):
    return [{
      'id':prods[i]['id'],
      'reference_id':refs[i]
    } for i in range(len(prods))]


class NNModel:
  
  def __init__(self) -> None:
    self.__embs = list()  # массив с ембедингами от эталонов


  def predict(self, inp: list):
    """
    в inp - dict 
      "product_id", "name", "props", "is_reference", "reference_id"
    """

    # your code here
    a = [{'id':i['id'], 'reference_id':i['id']} for i in inp]
    return a

  def add_embs(self, embs: list):
    # добавление новых ембедингов в озу модели
    """
    в inp - list[dict]
      "id", "name", "props"
    """
    self.__embs += embs

  def update_refs(self, refs: list):
    return refs


class NNModelManager:

  def __init__(
    self,
    nnmodel: NNModel, 
    db_model: models.models.Model = models.Reference, 
    *args, **kwargs
  ):
    self.nnmodel: NNModel = nnmodel
    self.db_model = db_model

  def update_refs(self, refs: list):
    if refs:
      model_refs = self.nnmodel.update_refs(refs)
      self.add_refs_embs(model_refs)
      for i in range(len(model_refs)):
        model_refs[i]['embends'] = pickle.dumps(model_refs[i]['embends'])
      self.write_refs(model_refs)

  def update_refs_clear(self, refs: list):
    if refs:
      model_refs = self.nnmodel.update_refs(refs)
      self.add_refs_embs(model_refs)
      self.write_refs(model_refs)


  def write_refs(self, refs: list):
    db_refs = list()
    for ref in refs:
      mm = self.db_model.objects.ref_create(ref)
      db_refs.append(mm)
    self.db_model.objects.bulk_create(db_refs)
    return db_refs

  def add_refs_embs(self, ref_embs: list):
    self.nnmodel.add_embs(ref_embs)


class RecModel(metaclass=Singletone):

  def __init__(self) -> None:
    self.model: NNModel = NNModel()
    self.model_manager: NNModelManager = NNModelManager(self.model)
    self.ser = JsonSer()
    self.load_embends()

  def predict(self, inp: list):
    ser_inp = self.ser.prepare(inp)
    pred_inp = self.model.predict(ser_inp)
    return pred_inp

  def update_embends(self, refs: list, clear: bool=True):
    ser_refs = self.ser.prepare(refs)
    if clear:
      self.model_manager.update_refs_clear(ser_refs)
    else:
      self.model_manager.update_refs(ser_refs)

  def load_embends(self):
    qs = list(self.model_manager.db_model.objects.values())
    self.update_embends(qs)


  def ex_predict(self, refs: list, targets: list):
    self.update_embends(refs, clear=False)
    return self.predict(targets)

  def mp_concat(self, prods: list, refs: list):
    return self.ser.mp_concat(prods, refs)

def ref_goods_split(data: list):
  refs, goods = [], []
  for d in data:
    if d['is_reference']:
      refs.append(d)
    else:
      goods.append(d)
  return refs, goods

