<template>
  <div class="checklists">
    <nav class="panel">
      <p class="panel-heading">
       Checklists
      </p>

      <div class="panel-block">
        <p class="control has-icons-left">
          <input class="input" type="text"
                 placeholder="To create a new checklist type the name and hit enter."
                 v-model="newChecklist"
                 @keyup.enter="addNewChecklist"
                 :disabled="saving"
          >
          <span class="icon is-left" v-if="saving">
            <i class="fa fa-spin fa-spinner"></i>
          </span>
        </p>
      </div>

      <div class="panel-block" v-for="checklist in checklists" :key="checklist.id">
        <router-link :to="{ name: 'checklist', params: { id: checklist.id }}">
          {{ checklist.name }}
        </router-link>
        <a class="button is-pulled-right is-danger"
           @click="removeChecklist(checklist)"
           :disabled="checklist.deleting"
        >
            <span class="icon">
              <i class="fa fa-spinner fa-spin" v-if="checklist.deleting"></i>
              <i class="fa fa-trash" v-else></i>
            </span>
        </a>
      </div>
    </nav>
  </div>
</template>

<script>
  import axios from 'axios';

  export default {
    name: 'checklists',
    data() {
      return {
        newChecklist: '',
        checklists: [],
        saving: false,
      };
    },
    created() {
      axios.get('/api/checklists')
        .then((response) => {
          this.checklists = response.data;
        })
        .catch(error => console.log(error));
    },
    methods: {
      addNewChecklist() {
        const checklist = this.newChecklist && this.newChecklist.trim();
        if (!checklist) {
          return;
        }
        this.saving = true;
        axios.post('/api/checklists', { name: this.newChecklist })
        .then((response) => {
          this.checklists.push(response.data);
          this.newChecklist = '';
          this.saving = false;
        })
        .catch((errors) => {
          this.saving = false;
          console.log(errors);
        });
      },
      removeChecklist(checklist) {
        const index = this.checklists.indexOf(checklist);
        const list = this.checklists[index];
        this.$set(list, 'deleting', true);
        axios.delete(`/api/checklists/${list.id}`)
        .then(() => {
          this.checklists.splice(index, 1);
          this.$set(list, 'deleting', false);
        })
        .catch((errors) => {
          console.log(errors);
          this.$set(list, 'deleting', false);
        });
      },
    },
  };
</script>

<style lang="scss" scoped="checklists">
  .panel-block { justify-content: space-between }
</style>
