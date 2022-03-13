import request from '@/utils/request'
import { tokenName } from '@/config'

export async function login(data) {
  return request({
    url: '/login',
    method: 'post',
    data,
  })
}

export async function socialLogin(data) {
  return request({
    url: '/socialLogin',
    method: 'post',
    data,
  })
}

export function getUserInfo(accessToken) {
  //此处为了兼容mock.js使用data传递accessToken，如果使用mock可以走headers
  return request({
    url: '/userInfo',
    method: 'post',
    data: {
      [tokenName]: accessToken,
    },
  })
}

export function getUserBalance(accessToken) {
  //此处为了兼容mock.js使用data传递accessToken，如果使用mock可以走headers
  return request({
    url: '/balance',
    method: 'post',
    data: {
      [tokenName]: accessToken,
    },
  })
}
export function getUserDiscount(accessToken) {
  //此处为了兼容mock.js使用data传递accessToken，如果使用mock可以走headers
  return request({
    url: '/discount',
    method: 'post',
    data: {
      [tokenName]: accessToken,
    },
  })
}

export function charge(accessToken, detail) {
  //此处为了兼容mock.js使用data传递accessToken，如果使用mock可以走headers
  return request({
    url: '/charge',
    method: 'post',
    data: {
      [tokenName]: accessToken,
      detail: detail,
    },
  })
}
export function paymentRequest(accessToken, order, mode) {
  //此处为了兼容mock.js使用data传递accessToken，如果使用mock可以走headers
  return request({
    url: '/pay',
    method: 'post',
    data: {
      [tokenName]: accessToken,
      order: order,
      mode: mode,
    },
  })
}

export function logout() {
  return request({
    url: '/logout',
    method: 'post',
  })
}

export function register() {
  return request({
    url: '/register',
    method: 'post',
  })
}
