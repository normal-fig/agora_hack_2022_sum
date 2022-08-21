from back_api import models

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
import pandas as pd
import numpy as np
from django.conf import settings


class Serializer:
  pass


class JsonSer(Serializer):
  
  def __init__(self) -> None:
    pass
  
  def prepare(self, items):
    return items

  def mp_concat(self, prods: list, refs: list, id_to_real:list):
    return [{
      'id':prods[i]['id'],
      'reference_id':id_to_real[refs[i]] if refs[i] != -1 else None
    } for i in range(len(prods))]


class NNModel:
  
  def __init__(self) -> None:
    self.embs = list()  
    self.ids = list()


  def predict(self, inp: list):
    goods_df = pd.DataFrame.from_dict(inp)
    
    embs_arr = []
    embs_arr.append(self.vectorizer_ch_name_tf.transform(goods_df['name']).toarray())
    embs_arr.append(self.vectorizer_wr_name_tf.transform(goods_df['name']).toarray())
    embs_arr.append(self.vectorizer_ch_props_tf.transform(goods_df['props']).toarray())
    embs_arr.append(self.vectorizer_wr_props_tf.transform(goods_df['props']).toarray())

    goods_embs = np.concatenate(embs_arr, axis=1)
    goods_embs = normalize(goods_embs, axis=1)

    etalons_embs = np.array(self.embs)

    ans = etalons_embs @ goods_embs.T
    mask = ans.max(axis=0) <= settings.MODEL_THRESHOLD
    y_pred = ans.argmax(axis=0)
    y_pred[mask] = -1

    # y = goods_df.join(pd.DataFrame(self.ids).reset_index().set_index(0), on='reference_id',how='left', lsuffix='_left', rsuffix='_right')['index'].values

    # from sklearn.metrics import accuracy_score
    # print(f"{ans.max(axis=0).min()=}")
    # with open(settings.MEDIA_ROOT / 'max.json', 'w') as out:
    #   import json
    #   json.dump(ans.max(axis=0).tolist(), out)
    # print(f"{settings.MODEL_THRESHOLD=}")
    # print(f"nulls: {mask.sum()}")
    # print(f"{accuracy_score(y[~mask],y_pred[~mask])=}")
    # m2 = y_pred != y
    # ids = np.array(self.ids)

    # with open(settings.MEDIA_ROOT / 'preds.json', 'w') as out:
    #   import json
    #   json.dump(ids[y[m2]].tolist(), out)
    #   json.dump(ids[y_pred[m2]].tolist(), out)
    return y_pred

  def add_embs(self, ids: list, embs: list):
    if embs:
      data_df = pd.DataFrame.from_dict(embs)

      vectorizer_ch_name_tf = TfidfVectorizer(analyzer='char', ngram_range=(1,5), max_df=1., min_df=1)
      vectorizer_wr_name_tf = TfidfVectorizer(analyzer='word', ngram_range=(1,4), max_df=2, min_df=1)
      vectorizer_ch_props_tf = TfidfVectorizer(analyzer='char', ngram_range=(1,2), max_df=1., min_df=1)
      vectorizer_wr_props_tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), max_df=1., min_df=1)

      self.vectorizer_ch_name_tf = vectorizer_ch_name_tf.fit(data_df['name'])
      self.vectorizer_wr_name_tf = vectorizer_wr_name_tf.fit(data_df['name'])
      self.vectorizer_ch_props_tf = vectorizer_ch_props_tf.fit(data_df['props'])
      self.vectorizer_wr_props_tf = vectorizer_wr_props_tf.fit(data_df['props'])

      embs_arr = []
      embs_arr.append(self.vectorizer_ch_name_tf.transform(data_df['name']).toarray())
      embs_arr.append(self.vectorizer_wr_name_tf.transform(data_df['name']).toarray())
      embs_arr.append(self.vectorizer_ch_props_tf.transform(data_df['props']).toarray())
      embs_arr.append(self.vectorizer_wr_props_tf.transform(data_df['props']).toarray())

      embs = np.concatenate(embs_arr, axis=1)
      embs = normalize(embs, axis=1)

      self.embs += list(embs)
      self.ids += ids

  def embends(self, refs: list):
    return refs

  def props_preprocess(self, refs: list):
    for ref in refs:
      ref['props'] = ' '.join(ref['props']).replace('\t', '')
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

  def _pop_ids(self, qs: list):
    return [i.pop('product_id') for i in qs]

  def load_refs_data(self):
    return list(self.db_model.objects.values())

  def add_embends(self, qs: list):
    ids = self._pop_ids(qs)
    embends = self.nnmodel.embends(qs)
    self.nnmodel.add_embs(ids, embends)
    return ids, embends

  def save_refs(self, refs: list):
    db_refs = list()
    for ref in refs:
      ref['product_id'] = ref.pop('id')
      mm = self.db_model.objects.ref_create(**ref)
      db_refs.append(mm)
    self.db_model.objects.bulk_create(db_refs)


class RecModel:

  def __init__(self) -> None:
    self.model: NNModel = NNModel()
    self.model_manager: NNModelManager = NNModelManager(self.model)
    self.ser = JsonSer()
    self._load_embends()


  def _load_embends(self):
    qs = self.model_manager.load_refs_data()
    self.model_manager.add_embends(qs)

  def predict(self, inp: list):
    ser_inp = self.ser.prepare(inp)

    self.model.props_preprocess(inp)
    pred_inp = self.model.predict(ser_inp)
    return pred_inp
  
  def update_embends(self, refs: list):
    ser_refs = self.ser.prepare(refs)
    self.model.props_preprocess(ser_refs)
    self.model_manager.save_refs(ser_refs)
    self.model_manager.add_embends(ser_refs)

recmodel = None

def get_recmodel():
  global recmodel
  if recmodel is None:
    recmodel = RecModel()
  return recmodel
  