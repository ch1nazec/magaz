<template>
    <div class="header">
        <div class="header__main">
        
            <div class="header__logo">
                <a href="/">
                    <img src="../assets/icon1.png" alt="ABCE">
                </a>
            </div>

            <div class="header__search">
                <input type="text">
                <div class="logo__loop">
                    <a href="/">
                        <img src="../assets/loop.png" alt="Поиск">
                    </a>
                </div>
            </div>

            <div class="header__right">
                <a href="about/" class="header__about">
                    <span>О нас</span>
                </a>

                <div class="other__logo">
                
                    <div class="logo__user">
                        <a href="">
                            <img src="../assets/userheader.svg" alt="Аккаунт">
                        </a>
                    </div>

                    <div class="logo__favourite">
                        <a href="">
                            <img src="../assets/favourite.svg" alt="Избранное">
                        </a>
                    </div>
                </div>

            </div>
        </div>
        <div class="header__category">
            <div class="section__categories">
                <section>Категории</section>
            </div>
            <div class="category" ref="scrollContainer">
                <a href="" class="category__a">Баскетбол </a>
                <a href="" class="category__a">Бег </a>
                <a href="" class="category__a">Скейтбординг</a>
                <a href="" class="category__a">Модные кроссовки</a>
                <a href="" class="category__a">Тренинг</a>
                <a href="" class="category__a">Туристические</a>
                <a href="" class="category__a">Ботинки</a>
                <a href="" class="category__a">Балетки</a>
                <a href="" class="category__a">Худи & свитшоты</a>
                <a href="" class="category__a">Куртки & пальто</a>
                <a href="" class="category__a">Свитеры</a>
                <a href="" class="category__a">Топы</a>
                <a href="" class="category__a">Баскетбол </a>
                <a href="" class="category__a">Бег </a>
                <a href="" class="category__a">Скейтбординг</a>
                <a href="" class="category__a">Модные кроссовки</a>
                <a href="" class="category__a">Тренинг</a>
                <a href="" class="category__a">Туристические</a>
                <a href="" class="category__a">Ботинки</a>
                <a href="" class="category__a">Балетки</a>
            </div>
            
            <div class="buttons">
                <button class="carousel-btn prev" @click="scroll('left')">Назад</button>
                <button class="carousel-btn next" @click="scroll('right')">Вперёд</button>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    methods: {
        scroll(offset) {
            const container = this.$refs.scrollContainer;
            const scrollAmount = 300;

                if (offset === 'left') {
        container.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
    } else {
        container.scrollBy({ left: scrollAmount, behavior: 'smooth' });
    }
        }
    }
}
</script>

<style scoped>

.header {
    font-family: 'Roboto', sans-serif;
    background: #82fff0;
    background: radial-gradient(circle,rgba(130, 255, 240, 0.59) 79%, rgba(253, 29, 29, 0) 100%, rgba(252, 176, 69, 0) 100%);
    border-bottom: 0.5px solid #DEDEDE;
}

.header__main {
    display: flex;
    justify-content: space-between;
    padding: 10px 350px;
}

img {
    width: 22px;
    height: 22px;
}

.header__logo img {
    width: 50px;
    height: 50px;
}

.header__search {
    display: flex;
    position: relative;
    max-width: 600px;
    flex: 1;
}

.header__search input {
    width: 100%;
    height: 38px;
    padding: 0 40px 0 15px;
    border-radius: 8px;
    border: 1px solid #ccc;
    outline: none;
    box-sizing: border-box;
}

.header__search .logo__loop {
    position: absolute;
    top: 7px;
    right: 10px;
    
}

.header__right {
    display: flex;
    justify-content: space-between;
    padding: 10px 10px;
    gap: 30px;

    .other__logo {
        display: flex;
        justify-content: space-between;
        gap: 20px;
    }
}

.header__about {
    :hover {
        color: aqua}
}

.header__category {
    display: flex;
    justify-content: space-evenly;
    align-items: center;

    display: flex;
    gap: 10px;
    position: relative;

    .category {
        position: relative;
        right: 200px;

        display: flex;
        overflow-x: auto;
        max-width: 900px;
        
        -ms-overflow-style: none;
        scrollbar-width: none;
        ::-webkit-scrollbar {
            display: none;
        }

        scroll-behavior: smooth;
        gap: 15px;
        flex: 1;
    }

    .category__a {
        flex: 0 0 auto;
        width: auto;
        padding: 10px 10px;
        white-space: nowrap;
    }

    .buttons {
        position: absolute;
        right: 300px;
        bottom: 5px;
        gap: 50px
    }

    .carousel-btn {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: none;
        background: #333;
        color: white;
        cursor: pointer;
    }
}
a {text-decoration: none;}
</style>