import { defineStore } from "pinia";
import api from "@/services/api";


export const useBrandsStore = defineStore('brands', {
    state: () => ({
        brands: [],
        brandsFilter: [],
        countTotal: 0,
        page: 1,
        pageFilter: 1,

        orderBy: '',
        searchQuery: '',

        loading: false,
        hasMore: true,

        brandProductSlug: '',

        nextPageURL: 'products/?page=1'

    }),
    actions: {
        async getBrands() {
            let url = 'brands/';
            while (url) {
                const response = await api.get(url);
                this.brands.push(...response.data.results);
                url = response.data.next;
            }
        },

        resetProductsBrand() {
            this.brandsFilter = []
            this.pageFilter = 1
            this.searchQuery = ''
            this.loading = false
            this.hasMore = true

            this.nextPageURL = 'products/?page=1'
        },

        async getProductsBrand(slug, reset = false) {
            if (this.loading) return;
            if (slug !== this.brandProductSlug) { reset = true}

            if (reset) {
                this.resetProductsBrand()
                this.brandProductSlug = slug
            }
            if (!this.hasMore && !reset) return

            try {
                this.loading = true

                const params = {
                    page: this.pageFilter,
                    ...(this.searchQuery && { search: this.searchQuery}),
                    ...(this.orderBy && { ordering: this.orderBy}),
                    ...(this.brandProductSlug && { brand__slug: this.brandProductSlug}),}

                const response = await api.get(`products/`, { params })
                let data = response.data.results
                this.countTotal = response.data.count

                if (reset) this.brandsFilter = data
                else this.brandsFilter.push(...data)
                
                this.hasMore = !!response.data.next
                this.nextPageURL = response.data.next

                if (this.hasMore) {this.pageFilter++}
            } catch (error) {console.log('Ошибка прогрузки продуктов по брендам: ', error)}
            finally { this.loading = false }
        },

        setOrderBy(value) {
            this.orderBy = value
            this.getProductsBrand(this.brandProductSlug, true)
        }
    }
})