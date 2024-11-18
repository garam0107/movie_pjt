<template>
  <footer class="footer">
    <div class="footer-content">
      <a href="#">서비스 이용약관</a> | <a href="#">회사 안내</a>
      <div class="contact-info">
        고객센터: cs@watchapedia.co.kr, 02-515-9985<br />
        제작 및 대외 협력: <a href="https://watcha.team/contact">https://watcha.team/contact</a><br />
        주식회사 왓챠 | 대표 박태훈 | 서울특별시 강남대로 343 신덕빌딩 3층<br />
        사업자 등록 번호: 211-88-66013
      </div>
      <div class="copyright">WATCHAPEDIA © 2024 by Watcha, Inc. All rights reserved.</div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
};
</script>

<style scoped>
.footer {
  width: 100%;
  background-color: #333;
  color: #fff;
  padding: 20px;
  text-align: center;
  font-size: 0.875rem;
  position: absolute;
  left: 0;
  bottom: 0;
}

.footer-content a {
  color: #fff;
  text-decoration: none;
  margin: 0 5px;
}

.footer-content a:hover {
  text-decoration: underline;
}

.contact-info {
  margin-top: 10px;
}

.copyright {
  margin-top: 10px;
}
</style>
