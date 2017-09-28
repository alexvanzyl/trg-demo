import Vue from 'vue';
import Router from 'vue-router';
import Checklists from '@/components/Checklists';
import Checklist from '@/components/Checklist';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '/',
      name: 'home',
      component: Checklists,
    },
    {
      path: '/:id',
      name: 'checklist',
      component: Checklist,
    },
  ],
});
