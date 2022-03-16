import request from '@/utils/request'

export function delItem(data) {
  return request({
    url: '/item/del',
    method: 'post',
    data: data,
  })
}
export function updateInventory(data) {
  return request({
    url: '/item/updateInventory',
    method: 'post',
    data: data,
  })
}
export function saveItem(data) {
  return request({
    url: '/item/save',
    method: 'post',
    data: data,
  })
}
export function getItems(params) {
  return request({
    url: '/table/getItems',
    method: 'get',
    params,
  })
}
export function getList(params) {
  return request({
    url: '/table/getList',
    method: 'get',
    params,
  })
}
export function getUsers(params) {
  return request({
    url: '/table/getUsers',
    method: 'get',
    params,
  })
}

export function doEdit(data) {
  return request({
    url: '/table/doEdit',
    method: 'post',
    data,
  })
}

export function doDelete(data) {
  return request({
    url: '/table/doDelete',
    method: 'post',
    data,
  })
}
