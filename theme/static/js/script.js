// custom scripts for carousel 

document.addEventListener("DOMContentLoaded", function () {
  // Hero Carousel initialization
  const heroSwiper = new Swiper('.swiper', {
    loop: true,
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.swiper-button-next',
      prevEl: '.swiper-button-prev',
    },
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
  });

  // Our Services Carousel initialization
  const serviceSwiper = new Swiper('.service-swiper', {
    loop: true,
    slidesPerView: 1,           // default for mobile
    spaceBetween: 20,
    pagination: {
      el: '.service-swiper .swiper-pagination',
      clickable: true,
    },
    navigation: {
      nextEl: '.service-swiper .swiper-button-next',
      prevEl: '.service-swiper .swiper-button-prev',
    },
    autoplay: {
      delay: 5000,
      disableOnInteraction: false,
    },
    breakpoints: {
      768: {
        slidesPerView: 3,       // 3 cards for desktop/tablet (≥768px)
      }
    }
  });
});
