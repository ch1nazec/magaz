import { defineStore } from "pinia";
import api from "@/services/api";


export const useCategoryStore = defineStore("category", {
    state: () => ({
        dataCategory: [],
        categoryTree: []
    }),
    actions: {
        async getCategories () {
        try {
            const response = await api.get('/api/categories/')
            this.dataCategory = response.data
        } catch (e) {console.log(e)}},
        
        async getCategoryTree () {
            try {
                const response = await api.get('/api/categories/tree/')
                this.categoryTree = response.data
            } catch (e) {console.log(e)}
        }
    }
})