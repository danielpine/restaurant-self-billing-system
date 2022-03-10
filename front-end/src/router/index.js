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

const fullRole = ['admin', 'member', 'visitor']
const visitor = ['visitor']
const member = ['member']
const admin = ['admin']

export const asyncRoutes = [
  {
    path: '/',
    component: Layout,
    redirect: '/index',
    meta: {
      title: '首页',
      icon: 'home-4-line',
      affix: true,
      roles: fullRole,
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
          roles: fullRole,
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
      roles: visitor,
    },
    children: [
      {
        path: 'pay',
        name: 'Pay',
        component: () => import('@/views/pay'),
        meta: {
          title: '自助结算',
          icon: 'exchange-cny-line',
          roles: visitor,
        },
      },
      {
        path: 'join',
        name: 'Join',
        component: () => import('@/views/join'),
        meta: {
          title: '加入会员',
          icon: 'vip-crown-2-line',
          roles: visitor,
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
      roles: member,
    },
    children: [
      {
        path: 'pay',
        name: 'MemberPay',
        component: () => import('@/views/pay'),
        meta: {
          title: '自助结算',
          icon: 'exchange-cny-line',
          roles: member,
        },
      },
      {
        path: 'recharge',
        name: 'recharge',
        component: () => import('@/views/member/Recharge'),
        meta: {
          title: '充值优惠',
          icon: 'battery-charge-fill',
          roles: member,
        },
      },
      {
        path: 'book',
        name: 'Book',
        component: () => import('@/views/member/Book'),
        meta: {
          title: '座位预订',
          icon: 'check-fill',
          roles: member,
        },
      },
    ],
  },
  {
    path: '/order',
    component: Layout,
    redirect: '/order/list',
    alwaysShow: true,
    meta: {
      title: '订单管理',
      icon: 'list-unordered',
      roles: admin,
    },
    children: [
      {
        path: 'list',
        name: 'list',
        component: () => import('@/views/order'),
        meta: {
          title: '历史订单',
          icon: 'history-line',
          roles: admin,
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
      roles: admin,
    },
    children: [
      {
        path: 'put',
        name: 'Put',
        component: () => import('@/views/admin/Put'),
        meta: {
          title: '菜品上架',
          icon: 'add-circle-line',
          roles: admin,
        },
      },
      {
        path: 'user',
        name: 'user',
        component: () => import('@/views/admin/User'),
        meta: {
          title: '用户管理',
          icon: 'user-settings-line',
          roles: admin,
        },
      },
      {
        path: 'inventory',
        name: 'inventory',
        component: () => import('@/views/admin/Inventory'),
        meta: {
          title: '库存管理',
          icon: 'database-2-line',
          roles: admin,
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
      roles: admin,
    },
    children: [
      {
        path: 'table',
        name: 'Table',
        component: () => import('@/views/vab/table'),
        meta: {
          title: '表格',
          icon: 'table-2',
          roles: admin,
        },
      },
      {
        path: 'icon',
        name: 'Icon',
        component: () => import('@/views/vab/icon'),
        meta: {
          title: '图标',
          icon: 'remixicon-line',
          roles: admin,
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
