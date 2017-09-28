<template>
  <div id="app">
    <div class="columns is-centered">
      <div class="column is-half is-narrow">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'app',
};
</script>

<style lang="scss">
@import "../node_modules/bulma/bulma.sass";
$fa-font-path: "../node_modules/font-awesome/fonts" !default;
@import "../node_modules/font-awesome/scss/font-awesome.scss";

#app { margin-top: 60px }
</style>
