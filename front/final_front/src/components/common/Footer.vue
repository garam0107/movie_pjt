<template>
  <footer class="footer">
    <div class="footer-content">
      <a href="#">서비스 이용약관</a> | <a href="#">프로젝트 안내</a>
      <div class="contact-info">
        고객센터: garam@gmail.com, 010-1234-5678<br />
        제작 및 대외 협력: <a href="https://watcha.team/contact">https://team.garam_jiin/contact</a><br />
        뮤비디비아 | 대표 이가람 | 1424호<br />
      </div>
      <div class="copyright">DOLDAM MOVIEDIA © 2024 by DolDam, Inc. All rights reserved.</div>
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
  position: relative;
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
