<template>
  <a-alert message="欢迎使用餐厅自助结算系统" type="success" show-icon />

  <a-card class="version-information">
    <template v-slot:title>系统信息</template>
    <template v-slot:extra>
      <a href="#">部署时间{{ updateTime }}</a>
    </template>
    <div class="version-information-table">
      <table>
        <tr style="background: lightgray;">
          <td>游客模块</td>
          <td>会员模块</td>
          <td>管理员模块</td>
        </tr>
        <tr>
          <td>
            <ul>
              <li>加入会员</li>
              <li>自助支付</li>
              <br />
            </ul>
          </td>
          <td>
            <ul>
              <li>自助支付</li>
              <li>充值优惠</li>
              <li>自助支付</li>
            </ul>
          </td>
          <td>
            <ul>
              <li>菜品上架</li>
              <li>用户管理</li>
              <li>库存管理</li>
            </ul>
          </td>
        </tr>
      </table>
    </div>
  </a-card>
  <a-card class="version-information">
    <template v-slot:title>优惠信息</template>
    <div class="version-information-table">
      <table>
        <tr style="background: lightgray;">
          <td>非会员</td>
          <td colspan="3" style="text-align: center;">会员</td>
        </tr>
        <tr>
          <td>
            不打折
          </td>
          <td>
            每月消费次数&lt;=5 : 不打折
          </td>
          <td>
            5&gt;每月消费次数&lt;=10 :打
            <span style="color: red;">95</span>
            折
          </td>
          <td>
            10&gt;每月消费次数 : 打
            <span style="color: red;">9</span>
            折
          </td>
        </tr>
      </table>
    </div>
  </a-card>
</template>
<script>
  import { dependencies, devDependencies } from '*/package.json'

  export default {
    data() {
      return {
        updateTime: process.env.VUE_APP_UPDATE_TIME,
        dependencies: dependencies,
        devDependencies: devDependencies,
      }
    },
  }
</script>
<style lang="less" scoped>
  .version-information {
    margin-top: @vab-margin;
    &-table {
      width: 100%;
      table {
        width: 100%;
        color: #666;
        border-collapse: collapse;
        background-color: #fff;

        td {
          position: relative;
          padding: 9px 15px;
          font-size: 14px;
          line-height: 20px;
          border: 1px solid #e6e6e6;
        }
      }
    }
  }
</style>
