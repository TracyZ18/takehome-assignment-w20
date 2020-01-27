<template>
  <p>
    I'm a Counter!
    <button v-on:click="count += 1">Add 1</button>
    <button v-on:click="count -= 1">Delete 1</button>
    The count is now {{ count }} !
  </p>
</template>

<script>
export default {
  props:["count"],
  data() {
    return {
      count: 0
    };
  }
};
</script>

<style>
</style>

