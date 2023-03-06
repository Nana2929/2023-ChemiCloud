import pandas as pd
from simpletransformers.classification import ClassificationModel, ClassificationArgs
import pandas as pd
import logging
import torch
from sklearn.metrics import classification_report
import re
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold
from imblearn.over_sampling import SMOTE
def find_chinese(file):
    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    chinese = re.sub(pattern, '', file)
    return chinese

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)
cuda_available=torch.cuda.is_available()
print(cuda_available)
NUM_EPOCH=20

all_df=pd.read_csv("all.csv")
all_df['content']=[find_chinese(i) for i in all_df['content']]


train_df=pd.read_csv("train.csv")
# train_df['content']=[find_chinese(i) for i in train_df['content']]

train_df['content']=[i for i in train_df['content']]
test_df=pd.read_csv("test.csv")
# test_df['content']=[find_chinese(i) for i in test_df['content']]
test_df['content']=[i for i in test_df['content']]
one_zero=lambda x: 1 if x=="食品安全" else 0

all_df['label']=[one_zero(i) for i in all_df['label']]
all_data=[[str(i)] for i in all_df['content']]
for e,i in enumerate(all_data):
    all_data[e].append(all_df['label'][e])

all_df = pd.DataFrame(all_data)
all_df.columns = ["text", "labels"]

train_df['label']=[one_zero(i) for i in train_df['label']]
train_data=[[str(i)] for i in train_df['content']]
for e,i in enumerate(train_data):
    train_data[e].append(train_df['label'][e])

train_df = pd.DataFrame(train_data)
train_df.columns = ["text", "labels"]



test_df['label']=[one_zero(i) for i in test_df['label']]
test_data=[[i] for i in test_df['content']]
for e,i in enumerate(test_data):
    test_data[e].append(test_df['label'][e])
eval_df = pd.DataFrame(test_data)
eval_df.columns = ["text", "labels"]
X_test=eval_df["text"]
X_test=[str(i) for i in X_test]
y_test=eval_df["labels"]
print(sum(train_df['labels']))
model_name='bert-base-chinese'

output_model=f"output_{model_name}_{NUM_EPOCH}"
model_args = ClassificationArgs(
            num_train_epochs=NUM_EPOCH,
            output_dir=output_model,
            use_multiprocessing=False,
            use_multiprocessing_for_evaluation=False,
            max_seq_length=512,
            
            )

model = ClassificationModel(
    "bert", model_name, args=model_args,use_cuda=cuda_available,weight=[1982/2088,106/2088]
)

import os

if __name__=='__main__':
    if not os.path.exists(f"output_{model_name}_{NUM_EPOCH}"):
        model.train_model(train_df)
        
    else:
        model = ClassificationModel(
                "bert", output_model,use_cuda=cuda_available
            )
        result, model_outputs, wrong_predictions = model.eval_model(
            eval_df
        )
        predictions, raw_outputs = model.predict(X_test)
        print(classification_report(predictions, y_test))
        print(accuracy_score(predictions, y_test))

        
def fold():
    NUM_EPOCH=20
    n=5
    kf = KFold(n_splits=n, random_state=42, shuffle=True)
    results = []
    model_args = ClassificationArgs(
        num_train_epochs=NUM_EPOCH,
        overwrite_output_dir=True,
        use_multiprocessing=False,
        use_multiprocessing_for_evaluation=False,
        max_seq_length=512
        )
    for train_index, val_index in kf.split(all_df):
    # splitting Dataframe (dataset not included)
        train_df = all_df.iloc[train_index]
        val_df = all_df.iloc[val_index]
        # Defining Model
        model = ClassificationModel("bert", model_name, args=model_args,use_cuda=cuda_available)
    # train the model
        model.train_model(train_df)
    # validate the model 
        result, model_outputs, wrong_predictions = model.eval_model(val_df, acc=accuracy_score)
        print(result['acc'])
    # append model score
        results.append(result['acc'])
    
    print("results",results)
    print(f"Mean-Precision: {sum(results) / len(results)}")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           

    
