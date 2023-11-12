<template>
  <div>
    <div class="row align-items-center text-center" style="height: 30rem;">
      <div class="col-12 col-md-5">
        <div>
          <img src="@/assets/landing_cake.png" class="img-fluid w-75" alt="image cake">
        </div>
      </div>
      <div class="col-12 col-md-7">
        <div>
          <h1 class="my-2 logo">Fun Cake</h1>
          <h5 class="my-2 text-cake text-cake-bold">Больше, чем просто торт</h5>
          <cake-button class="btn-cake" @click="$router.push('/cakes')">Смотреть каталог</cake-button>
        </div>
      </div>
    </div>

    <div class="row align-items-center text-center" style="height: 15rem;">
      <div class="col-12 offset-12">
        <div>
          <h2 class="my-3 text-cake text-cake-bold">Обо мне</h2>
          <h6 class="my-2 text-cake text-cake-light">Привет! Меня зовут
            <strong>Наталья</strong>, я домашний кондитер в Перми.</h6>
          <h6 class="my-2 text-cake text-cake-light">В приготовлении использую <strong>только
            натуральные и свежие</strong> ингредиенты.</h6>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
@font-face {
  font-family: rose;
  src: url('@/assets/ttf/rose.ttf');
}

@font-face {
  font-family: open-sans-bold;
  src: url('@/assets/ttf/open-sans-bold.ttf');
}

@font-face {
  font-family: open-sans-light;
  src: url('@/assets/ttf/open-sans-light.ttf');
}

.logo {
  font-family: rose, serif;
  font-weight: bolder;
  font-size: 4rem;
  color: #444251;
}

.text-cake {
  color: #444251;
}

.text-cake-bold {
  font-family: open-sans-bold, serif;
}

.text-cake-light {
  font-family: open-sans-light, serif;
}

</style>