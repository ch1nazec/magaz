<template>
    <div class="footer-main">
        <div class="footer-main__container">
            <div class="footer-main__info">
                <div class="info__abce">
                    <p>ABCE Store<br>№1 по г. Уссурийск</p>
                </div>
                <div class="info__other-info">
                    <p>Тут ещё что-то должно быть, но я ещё не придумал</p>
                </div>
                <div class="info__phone-number">
                    <p>228-143-155</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>

</script>

<style scoped>
.footer-main {
    background-color: black;
    display: flex;
    flex-direction: column;
    justify-content: center;}

.footer-main__container {
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;}

.footer-main__info {
    padding: 40px 50px;
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 20px;}

.footer-main p {
    color: white;
    margin: 0;}

@media (max-width: 768px) {
    .footer-main__info {
        flex-direction: column;
        text-align: center;
        padding: 30px 20px;
        gap: 20px;}
    
    .info__other-info,
    .info__other-number {
        align-self: center !important;}
    
    .footer-main p {
        font-size: 14px;}
}
</style>