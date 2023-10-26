from flask import Flask, render_template, request
import pandas as pd
import csv
from sklearn.cluster import dbscan
import matplotlib.pyplot as plt
import dbscan

import re
from sklearn.cluster import DBSCAN
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from io import BytesIO
import base64
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
        

app = Flask(__name__)

# def predictor():
#     df = pd.read_csv('HasilPreProcess.csv')
#     df.to_pickle('df.pkl')    #to save the dataframe, df to 123.pkl
#     pkl = pd.read_pickle('df.pkl') #to load 123.pkl back to the dataframe df
#     return pkl

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/readtable')
def readtable():
    with open("HasilPreProcess.csv") as file:
        reader = csv.reader(file)
        return render_template("readtable.html", csv=reader)

@app.route('/calculate', methods=['POST'])
def calculate():
    if request.method == "POST":
       data = request.form.get("data")
       epsilon = request.form['eps']
       minpoints = request.form['minpts']

       
    # # PCA merupakan reduksi fitur
    # # Disini hanya berfungsi agar mudah untuk dilakukan visualisasi menggunakan scatter plot
    # pca = PCA(n_components=2)
    # X_pca = pca.fit_transform(f_data)
    # dbscan = DBSCAN(eps={epsilon}, min_samples={minpoints})
    # dbscan_labels = dbscan.fit_predict(X_pca)
    # dbscan_n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
    # # print("Estimated number of DBSCAN clusters: %d" % dbscan_n_clusters)

    return render_template("calculate.html", eps=epsilon, minpts=minpoints)



# df = pd.read_csv('HasilPreProcess.csv', delimiter=',')
# df = pd.DataFrame(df)
# match_gejala = ['covid','sars-cov-2','corona','batuk','batuk kering','pilek',
#                 'kelelahan','sakit kepala','demam','sesak nafas','omicron',
#                 'delta','tenggorokan','anosmia','diare']

# # Membuat kolom baru yang mana nanti digunakan untuk menampung frekuensi disetiap gejalas
# for i in match_gejala:
#     df[i] = 0
    
# # Fungsi untuk menghitung frekuensi
# def getFrekuensi(data, match_gejala):
#     temp = str(data).split()
#     regex_pattern = r"\b(" + "|".join(match_gejala) + r")\b"
#     matching = [s for s in temp if re.search(regex_pattern, s)]
#     return matching

# # Proses pengambilan kolom final_tweet
# for idx in range(len(df["final_tweet"])):
#     freq = {}
#     # Hitung frekuensi tiap record
#     mask = getFrekuensi(df["final_tweet"][idx],match_gejala)        
#     for i in mask:
#         if i in freq.keys():
#             freq[i] = 1 + freq[i]
#         else:
#             freq[i] = 1    
    
#     for key,value in freq.items():
#         df.iloc[idx, df.columns.get_loc(key)] = value
# #proses DBSCAN
# # Inisialisasi kolom yang akan diproses
# list_features = ['covid', 'sars-cov-2', 'corona', 'batuk', 'batuk kering',
#     'pilek', 'kelelahan', 'sakit kepala', 'demam', 'sesak nafas', 'omicron',
#     'delta', 'tenggorokan', 'anosmia', 'diare']
# f_data = df[list_features]

# # Inisialisasi kolom yang akan di tampilkan di geovisualisasi       
# label_id = ['latitude','longitude','username','final_tweet']
# id_data = df[label_id]



# @app.route('/plot.png')
# def get_plot():
#     fig = Figure()
#     fig, axs = plt.subplots(1, 1, figsize=(10, 20))
#     axs[1].scatter(X_pca[dbscan_labels!=-1, 0], 
#                    X_pca[dbscan_labels!=-1, 1], 
#                    c=dbscan_labels[dbscan_labels!=-1], cmap='viridis')
#     axs[1].scatter(X_pca[dbscan_labels==-1, 0], 
#                    X_pca[dbscan_labels==-1, 1], 
#                    c='grey', alpha=0.5, marker='x')
#     axs[1].set_title(f"Estimated number of clusters: {dbscan_n_clusters}")

#     output = io.BytesIO()
#     FigureCanvasAgg(fig).print_png(output)
#     return Response(output.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(debug=True)

# return udah works.
# return nanti diganti dengan inputan rumus perhitungan DBSCAN.
# bikin output plot dan maps penyebarannya

# result = plot dbscan
# kasih tombol maps di calculate.html as an input for mapping folium