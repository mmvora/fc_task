import pandas as pd
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA


from fc_task.config import load_db_url
from fc_task.article_model import Article


def create_clusters() -> None:
    engine = create_engine(load_db_url())

    with Session(engine) as session:
        articles = session.query(Article).all()

    # create a dataframe of the article titles and summaries
    df = pd.DataFrame(
        [(article.title, article.ai_summary) for article in articles],
        columns=["title", "summary"],
    )

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["summary"])

    # inertias = []
    # K = range(1, 10)
    # for k in K:
    #     kmeans = KMeans(n_clusters=k, random_state=42)
    #     kmeans.fit(X)
    #     inertias.append(kmeans.inertia_)

    # plt.figure(figsize=(8, 5))
    # plt.plot(K, inertias, marker='o')
    # plt.title('Elbow Method for Optimal k')
    # plt.xlabel('Number of Clusters')
    # plt.ylabel('Inertia')
    # plt.show()

    optimal_k = 3
    kmeans = KMeans(n_clusters=optimal_k, random_state=42)
    kmeans.fit(X)

    df["cluster"] = kmeans.labels_

    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X.toarray())

    df["x"] = X_reduced[:, 0]
    df["y"] = X_reduced[:, 1]
    # Reduce dimensions for visualization
    pca = PCA(n_components=2)
    X_reduced = pca.fit_transform(X.toarray())

    plt.figure(figsize=(12, 8))
    colors = plt.cm.get_cmap("viridis", optimal_k)

    for i in range(optimal_k):
        cluster_data = df[df["cluster"] == i]
        plt.scatter(
            cluster_data["x"], cluster_data["y"], color=colors(i), label=f"Cluster {i}"
        )

        # Annotate each point with the title
        for j in range(cluster_data.shape[0]):
            plt.text(
                cluster_data["x"].iloc[j],
                cluster_data["y"].iloc[j],
                cluster_data["title"].iloc[j],
                fontsize=9,
            )

    plt.title("K-means Clustering of Article Summaries with Titles")
    plt.xlabel("PCA Component 1")
    plt.ylabel("PCA Component 2")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    create_clusters()
