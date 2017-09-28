<template>
  <div class="checklist">
    <router-link class="button" :to="{name: 'home'}">
      <span class="icon"><i class="fa fa-home"></i></span>
    </router-link>
    <nav class="panel">
      <p class="panel-heading">
        {{ checklist.name }}
      </p>

      <div class="panel-block">
        <p class="control has-icons-left">
          <input class="input" type="text"
                 placeholder="To add a new item to the list type the name and hit enter."
                 v-model="newItem"
                 @keyup.enter="addItem"
                 :disabled="saving"
          >
          <span class="icon is-left" v-if="saving">
            <i class="fa fa-spin fa-spinner"></i>
          </span>
        </p>
      </div>

      <a class="panel-block" v-for="checklistItem in checklistItems"
         :key="checklistItems.id"
         @click="toggleChecked(checklistItem)"
      >
        <span :class="{'is-check': checklistItem.is_check}">
          {{ checklistItem.name }}
        </span>
        <a class="button is-right is-danger"
           @click="removeItem(checklistItem)"
           :disabled="checklistItem.deleting"
        >
          <span class="icon">
            <i class="fa fa-spinner fa-spin" v-if="checklistItem.deleting"></i>
            <i class="fa fa-trash" v-else></i>
          </span>
        </a>
      </a>
    </nav>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'checklist',
    data() {
      return {
        checklist: {},
        newItem: '',
        checklistItems: [],
        saving: false,
      };
    },
    created() {
      axios.get(`/api/checklists/${this.$route.params.id}`)
          .then((response) => {
            this.checklist = response.data;
            this.checklistItems = response.data.items;
          })
          .catch(error => console.log(error));
    },
    methods: {
      addItem() {
        const item = this.newItem && this.newItem.trim();
        if (!item) {
          return;
        }
        this.saving = true;
        axios.post(`/api/checklists/${this.$route.params.id}/items`, {
          name: this.newItem,
        })
        .then((response) => {
          this.checklistItems.push(response.data);
          this.newItem = '';
          this.saving = false;
        })
        .catch((errors) => {
          this.saving = true;
          console.log(errors);
        });
      },
      toggleChecked(checklistItem) {
        const index = this.checklistItems.indexOf(checklistItem);
        const item = this.checklistItems[index];
        this.$set(item, 'is_check', !item.is_check);

        axios.patch(`/api/checklists/${this.$route.params.id}/items/${item.id}`, {
          is_check: item.is_check,
        });
      },
      removeItem(checklistItem) {
        const index = this.checklistItems.indexOf(checklistItem);
        const item = this.checklistItems[index];
        this.$set(item, 'deleting', true);
        axios.delete(`/api/checklists/${this.$route.params.id}/items/${item.id}`)
        .then(() => {
          this.checklistItems.splice(index, 1);
          this.$set(item, 'deleting', false);
        });
      },
    },
  };
</script>

<style lang="scss" scoped="checklists">
  .panel-block { justify-content: space-between }
  .is-check { text-decoration: line-through }
</style>