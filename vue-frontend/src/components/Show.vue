<template>
  <!-- PART 4: Add your code here -->
  <div>
    The name of the show is {{ name }}. Episodes seen: {{episodes_seen}}
    <counter :count="episodes_seen"></counter>
  </div>
</template>

<script>
// PART 4: Add your code here
import Counter from "./Counter.vue";

export default {
  components: {
    Counter
  },
  props: ["id","name","episodes_seen"]
};
</script>

<style>
</style>
