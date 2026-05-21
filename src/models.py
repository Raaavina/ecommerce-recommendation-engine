# src/models.py
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

class HybridRecommender:
    def __init__(self, user_item_matrix):
        self.user_item_matrix = user_item_matrix
        print("Computing live user similarity projections...")
        similarity_array = cosine_similarity(user_item_matrix)
        self.similarity_df = pd.DataFrame(
            similarity_array, 
            index=user_item_matrix.index, 
            columns=user_item_matrix.index
        )

    def get_candidates(self, target_user, top_n_items=5):
        if target_user not in self.user_item_matrix.index:
            # Cold start safety fall-back: return top popular items globally
            return ["85123A", "22423", "85099B", "47566", "20725"]
            
        similar_users = self.similarity_df[target_user].sort_values(ascending=False).iloc[1:11].index
        peer_purchases = self.user_item_matrix.loc[similar_users]
        scores = peer_purchases.sum(axis=0)
        
        already_bought = self.user_item_matrix.loc[target_user]
        unseen_items = scores.drop(labels=already_bought[already_bought > 0].index)
        
        return unseen_items.sort_values(ascending=False).head(top_n_items).index.tolist()