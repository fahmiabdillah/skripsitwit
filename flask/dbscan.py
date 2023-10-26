# import pandas as pd
# import re
# from sklearn.cluster import DBSCAN
# import matplotlib.pyplot as plt
# import numpy as np
# from sklearn.preprocessing import StandardScaler

# import app

# new_eps = app.eps
# new_minpts = app.minpts

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

# # PCA merupakan reduksi fitur
# # Disini hanya berfungsi agar mudah untuk dilakukan visualisasi menggunakan scatter plot
# from sklearn.decomposition import PCA
# pca = PCA(n_components=2)
# X_pca = pca.fit_transform(f_data)

# dbscan = DBSCAN(eps={{new_eps}}, min_samples={{new_minpts}}) #default parameters are eps = 0.5, min_samples = 5, metric = 'euclidean'
# dbscan_labels = dbscan.fit_predict(X_pca)
# dbscan_n_clusters = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
# print("Estimated number of DBSCAN clusters: %d" % dbscan_n_clusters)

