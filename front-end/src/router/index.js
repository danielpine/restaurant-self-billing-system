import { createRouter, createWebHashHistory } from 'vue-router'
import Layout from '@/layout'

export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login'),
    hidden: true,
  },
  {
    path: '/403',
    name: '403',
    component: () => import('@/views/403'),
    hidden: true,
  },
  {
    path: '/404',
    name: '404',
    component: () => import('@/views/404'),
    hidden: true,
  },
]
export const asyncRoutes = [
  {
    path: '/',
    component: Layout,
    redirect: '/index',
    meta: {
      title: '首页',
      icon: 'home-4-line',
      affix: true,
    },
    children: [
      {
        path: 'index',
        name: 'Index',
        component: () => import('@/views/index'),
        meta: {
          title: '首页',
          icon: 'home-4-line',
          affix: true,
        },
      },
    ],
  },
  {
    path: '/visitor',
    component: Layout,
    redirect: '/visitor/pay',
    alwaysShow: true,
    meta: {
      title: '游客模块',
      icon: 'bubble-chart-line',
    },
    children: [
      {
        path: 'pay',
        name: 'Pay',
        component: () => import('@/views/pay'),
        meta: {
          title: '自助结算',
          icon: 'exchange-cny-line',
        },
      },
      {
        path: 'join',
        name: 'Join',
        component: () => import('@/views/join'),
        meta: {
          title: '加入会员',
          icon: 'vip-crown-2-line',
        },
      },
    ],
  },
  {
    path: '/member',
    component: Layout,
    redirect: '/member/pay',
    alwaysShow: true,
    meta: {
      title: '会员模块',
      icon: 'vip-line',
    },
    children: [
      {
        path: 'pay',
        name: 'MemberPay',
        component: () => import('@/views/pay'),
        meta: {
          title: '自助结算',
          icon: 'exchange-cny-line',
        },
      },
      {
        path: 'recharge',
        name: 'recharge',
        component: () => import('@/views/member/Recharge'),
        meta: {
          title: '充值优惠',
          icon: 'battery-charge-fill',
        },
      },
      {
        path: 'book',
        name: 'Book',
        component: () => import('@/views/member/Book'),
        meta: {
          title: '座位预订',
          icon: 'check-fill',
        },
      },
    ],
  },
  {
    path: '/admin',
    component: Layout,
    redirect: '/admin/put',
    alwaysShow: true,
    meta: {
      title: '管理模块',
      icon: 'admin-line',
    },
    children: [
      {
        path: 'put',
        name: 'Put',
        component: () => import('@/views/admin/Put'),
        meta: {
          title: '菜品上架',
          icon: 'add-circle-line',
        },
      },
      {
        path: 'user',
        name: 'user',
        component: () => import('@/views/admin/User'),
        meta: {
          title: '用户管理',
          icon: 'user-settings-line',
        },
      },
      {
        path: 'inventory',
        name: 'inventory',
        component: () => import('@/views/admin/Inventory'),
        meta: {
          title: '库存管理',
          icon: 'database-2-line',
        },
      },
    ],
  },
  {
    path: '/vab',
    component: Layout,
    redirect: '/vab/table',
    alwaysShow: true,
    meta: {
      title: '组件',
      icon: 'apps-line',
    },
    children: [
      {
        path: 'table',
        name: 'Table',
        component: () => import('@/views/vab/table'),
        meta: {
          title: '表格',
          icon: 'table-2',
        },
      },
      {
        path: 'icon',
        name: 'Icon',
        component: () => import('@/views/vab/icon'),
        meta: {
          title: '图标',
          icon: 'remixicon-line',
        },
      },
    ],
  },
  // {
  //   path: '/test',
  //   component: Layout,
  //   redirect: '/test/test',
  //   meta: {
  //     title: '动态路由测试',
  //     icon: 'test-tube-line',
  //   },
  //   children: [
  //     {
  //       path: 'test',
  //       name: 'Test',
  //       component: () => import('@/views/test'),
  //       meta: {
  //         title: '动态路由测试',
  //         icon: 'test-tube-line',
  //       },
  //     },
  //   ],
  // },
  // {
  //   path: '/error',
  //   name: 'Error',
  //   component: Layout,
  //   redirect: '/error/403',
  //   meta: {
  //     title: '错误页',
  //     icon: 'error-warning-line',
  //   },
  //   children: [
  //     {
  //       path: '403',
  //       name: 'Error403',
  //       component: () => import('@/views/403'),
  //       meta: {
  //         title: '403',
  //         icon: 'error-warning-line',
  //       },
  //     },
  //     {
  //       path: '404',
  //       name: 'Error404',
  //       component: () => import('@/views/404'),
  //       meta: {
  //         title: '404',
  //         icon: 'error-warning-line',
  //       },
  //     },
  //   ],
  // },
  // {
  //   path: '/*',
  //   redirect: '/404',
  //   hidden: true,
  // },
]
const router = createRouter({
  history: createWebHashHistory(),
  routes: constantRoutes,
})

export default router
