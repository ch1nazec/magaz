import { defineStore } from "pinia";
import api from "@/services/api";


export const useProducts = defineStore('product', {
    state: () => ({
        product: [],

        products: [],
        productsVariant: [],
        productsForCategoryList: [],

        brands: [],
        categoryProductSlug: '',

        currentPage: 1,
        currentPageVariant: 1,
        currentPageCategory: 1,

        hasMore: true,
        hasMoreVariant: true,
        hasMoreCategory: true,

        searchQuery: '',
        orderBy: '',
        categorySlug: '',

        loading: false,
        loadingProduct: false,
        loadingVariants: false,
        loadingCategory: false,

        nextPageURL: 'products/?page=1',
        nextPageURLVariant: 'productvariants/?page=1',
        nextPageURLCategory: 'product-category/',
    }),

    actions: {
        resetProduct() {
            this.product = [],
            this.loadingProduct = false},

        resetProducts() {
            this.products = [],
            this.currentPage = 1,
            this.hasMore = true,
            this.nextPageURL = 'products/?page=1'},

        resetVariantsProduct() {
            this.productsVariant = [],
            this.currentPageVariant = 1,
            this.hasMoreVariant = true,
            this.nextPageURLVariant = 'productvariants/?page=1'},
        
        resetCategoryProduct() {
            this.categoryProductSlug = '',
            this.productsForCategoryList = [],
            this.currentPageCategory = 1,
            this.hasMoreCategory = true,
            this.nextPageURLCategory = 'product-category/'
        },

        async getProduct(reset = true) {
            
        },

        async getAllProduct(reset = false) {
            if (this.loading) return
            if (reset) this.resetProducts()
            
            if (!this.hasMore && !reset) return

            this.loading = true

            try {
                const params = {
                    page: this.currentPage,
                    ...(this.searchQuery && { search: this.searchQuery }),
                    ...(this.orderBy && { ordering: this.orderBy }),
                    ...(this.categorySlug && { category: this.categorySlug })
                }

                const response = await api.get('products/', { params })

                if (reset) {
                    this.products = response.data.results}
                else { this.products.push(...response.data.results) }

                this.hasMore = !!response.data.next
                this.nextPageURL = response.data.next

                if (this.hasMore) {
                    this.currentPage++
                }
            } catch (error) {console.log('Ошибка загрузки товаров: ', error)}
            finally { this.loading = false }
        },

        async getAllProductsVariant(reset = false) {
            if (this.loadingVariants) return
            if (reset) this.resetVariantsProduct()

            if (!this.hasMoreVariant && !reset) return

            this.loadingVariants = true
            try {
                const params = {
                    page: this.currentPageVariant,
                    ...(this.searchQuery && { search: this.searchQuery }),
                    ...(this.orderBy && { ordering: this.orderBy }),
                    ...(this.categorySlug && { category: this.categorySlug })}
                
                const response = await api.get('productvariants/', { params })
                
                if (reset) {
                    this.productsVariant = response.data.results}
                else {this.productsVariant.push(...response.data.results)}
                
                    this.hasMoreVariant = !!response.data.next
                    this.nextPageURLVariant = response.data.next

                    if (this.hasMoreVariant) { this.currentPageVariant++ }
            } catch (error) {console.log(`Ошибка в прогрузке варинатов продуктов: ${error}`)}
            finally { this.loadingVariants = false }
        },

        async getProductCategory(slug, reset = false, brands = "") {
            if (this.loadingCategory) return
            if (slug !== this.categoryProductSlug) { reset = true}

            if (reset) {
                this.resetCategoryProduct()
                this.categoryProductSlug = slug
            }

            if (!this.hasMoreCategory && !reset) return
            this.loadingCategory = true
            try {
                const params = {
                    page: this.currentPageCategory,
                    ...(this.searchQuery && { search: this.searchQuery }),
                    ...(this.orderBy && { ordering: this.orderBy }),
                    ...(brands && { brand: brands})}

                    const response = await api.get(`product-category/${this.categoryProductSlug}/`, { params })

                    if (reset) {this.productsForCategoryList = response.data.results}
                    else {this.productsForCategoryList.push(...response.data.results)}

                    this.hasMoreCategory = !!response.data.next
                    this.nextPageURLCategory = response.data.next

                    this.brands = response.data.available_brands

                    if (this.hasMoreCategory) { this.currentPageCategory++ }
                } catch (error) {console.log(`Ошибка загрузки продуктов по категориям: ${error}`)}
            finally { this.loadingCategory = false }
        },

        async sendToCart(data) {
            if (this.loading) return
            this.loading = true

            try {
                const response = await api.post(`cart/`, data)
                console.log(response)    
            } catch (error) {
                console.error(error)}
            finally {
                this.loading = false}},

        async getProduct(slug, reset = false) {
            if (!slug) return;

            if (this.loadingProduct) return;
            if (reset) {this.resetProduct()}

            try {
                this.loadingProduct = true
                const response = await api.get(`productvariants/?search=${slug}`)

                this.product = [...response.data.results]
            } catch (error) {
                console.log('Ошибка при отправки API к продукту: ', error)}
            finally {this.loadingProduct = false}},
        
        async getCart() {
            if (this.loading) return

            this.loading = true
            try {
                const response = await api.get(`cart/`)
                return response.data
            } catch (error) {
                console.error(error)}
            finally {this.loading = false}
        },

        async postOrder() {
            if (this.loading) return

            this.loading = true
            try {
                const response = await api.post(`order/`)
            } catch (error) {
                console.error(error)}
            finally {this.loading = false}
        },

        setOrderBy(order) {
            this.orderBy = order
            this.getAllProduct(true)},
        
        setSearchQuery(query) {
            this.searchQuery= query},

        setOrderCatBy(slug, order) {
            this.orderBy = order
            this.getProductCategory(slug, true)},
        
        setSearchCatQuery(slug, query) {
            this.searchQuery= query
            this.getProductCategory(true, slug)
        },

        setOrderVariantBy(order) {
            this.orderBy = order
            this.getAllProductsVariant(true)},
        
        setSearchVariantQuery(query) {
            this.searchQuery= query
            this.getAllProductsVariant(true)
        },
    },

    getters: {
        productsCount: (state) => state.products.length,
        hasProducts: (state) => state.products.length > 0,
        isLoaded: (state) => state.products.length > 0 || !state.hasMore}
})