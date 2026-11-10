import { createRouter, createWebHistory } from 'vue-router'
import DeskView from '@/views/Desk.vue'
import TestView from '@/views/TestView.vue'
import Management from '@/sidebar_tabs/Management.vue'
import Maintenance from '@/sidebar_tabs/Maintenance.vue'
import HR from '@/sidebar_tabs/HR.vue'
import Safety from '@/sidebar_tabs/Safety.vue'
import Warehouse from '@/sidebar_tabs/Warehouse.vue'
import CustomerSLA from '@/sidebar_tabs/CustomerSLA.vue'
import Operations from '@/sidebar_tabs/Operations.vue'

// Live DB Test Views (for /test testing area)
import TestDeskView from '@/views_test/TestDesk.vue'
import TestManagement from '@/views_test/sidebar_tabs/Management.vue'
import TestMaintenance from '@/views_test/sidebar_tabs/Maintenance.vue'
import TestHR from '@/views_test/sidebar_tabs/HR.vue'
import TestSafety from '@/views_test/sidebar_tabs/Safety.vue'
import TestOperations from '@/views_test/sidebar_tabs/Operations.vue'

const routes = [
  {
    path: '/test',
    component: TestDeskView,
    children: [
      {
        path: '',
        redirect: '/test/management'
      },
      {
        path: 'management',
        name: 'test-management',
        component: TestManagement,
      },
      {
        path: 'maintenance',
        name: 'test-maintenance',
        component: TestMaintenance,
      },
      {
        path: 'hr',
        name: 'test-hr',
        component: TestHR,
      },
      {
        path: 'safety',
        name: 'test-safety',
        component: TestSafety,
      },
      {
        path: 'operations',
        name: 'test-operations',
        component: TestOperations,
      },
      {
        path: 'sandbox',
        name: 'test-sandbox',
        component: TestView,
      }
    ]
  },
  {
    path: '/',
    component: DeskView,
    children: [
      {
        path: '',
        redirect: 'management'
      },
      {
        path: 'management',
        name: 'management',
        component: Management,
      },
      {
        path: 'maintenance',
        name: 'maintenance',
        component: Maintenance,
      },
      {
        path: 'hr',
        name: 'hr',
        component: HR,
      },
      {
        path: 'safety',
        name: 'safety',
        component: Safety,
      },
      {
        path: 'warehouse',
        name: 'warehouse',
        component: Warehouse,
      },
      {
        path: 'customer-sla',
        name: 'customer-sla',
        component: CustomerSLA,
      },
      {
        path: 'operations',
        name: 'operations',
        component: Operations,
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory('/dashboard'),
  routes,
})

export default router
