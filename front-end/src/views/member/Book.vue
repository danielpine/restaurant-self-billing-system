<template>
  <div class="index-container">
    <a-card style="width: 800px; margin: 0 auto;">
      <div style="background: green;">
        <a-row>
          <a-col :span="6">
            <h3 style="color: white;">
              <vab-icon :icon="'calendar-check-line'"></vab-icon>
              座位预订
            </h3>
          </a-col>
        </a-row>
        <a-row style="width: 100%; color: white; font-size: 8px;">
          1.预订座位当日当时段有效，过期作废。
        </a-row>
        <a-row style="width: 100%; color: white; font-size: 8px;">
          2.选择日期时段区域，点击预订。
        </a-row>
      </div>
      <a-card style="width: 100%; margin: 0 auto;">
        <br />
        <br />
        <a-row v-if="booked">
          <a-col :span="4" style="padding-left: 10px;">
            <vab-icon :icon="'calendar-2-line'"></vab-icon>
            当前预订：
          </a-col>
          <a-col :span="6" style="padding-left: 10px; color: green;">
            {{ booked.book_date + ' ' + booked.book_time }}
          </a-col>
          <a-col :span="3" style="padding-left: 10px;">
            <a-button size="small" @click="unbooking">Cancel</a-button>
          </a-col>
          <a-col :span="3" style="padding-left: 10px;">
            <a-button size="small" @click="usebooking">Check</a-button>
          </a-col>
        </a-row>
        <br />
        <br />
        <a-row class="charge">
          <a-col :span="4" style="padding-left: 10px;">
            <vab-icon :icon="'calendar-2-line'"></vab-icon>
            预订日期：
          </a-col>
          <a-col :span="6" style="padding-left: 10px;">
            <a-date-picker
              @change="onDateChange"
              :default-value="moment(book.date, 'YYYY-MM-DD')"
            />
          </a-col>
        </a-row>
        <br />
        <br />
        <a-row class="charge">
          <a-col :span="4" style="padding-left: 10px;">
            <vab-icon :icon="'time-line'"></vab-icon>
            预订时段：
          </a-col>
          <a-col :span="20">
            <a-radio-group :default-value="1" size="large" @change="onChange">
              <a-radio-button :value="1">
                <div style="font-size: 16px; color: orange;">
                  7:00-10:00
                </div>
              </a-radio-button>
              <a-radio-button :value="2">
                <div style="font-size: 16px; color: orange;">
                  11:00-13:00
                </div>
              </a-radio-button>
              <a-radio-button :value="3">
                <div style="font-size: 16px; color: orange;">
                  17:00-19:00
                </div>
              </a-radio-button>
            </a-radio-group>
          </a-col>
        </a-row>
        <br />
        <br />
        <br />
        <a-row class="charge">
          <a-button type="primary" style="margin: 0 auto;" @click="booking">
            立即预订
          </a-button>
        </a-row>
        <br />
        <br />
      </a-card>
    </a-card>
  </div>
</template>

<script>
  import VabIcon from '@/layout/vab-icon'
  import { booking, getbooking, usebooking, unbooking } from '@/api/user'
  import { getAccessToken } from '@/utils/accessToken'
  import { useStore } from 'vuex'
  import { computed } from 'vue'
  import { message } from 'ant-design-vue'
  import moment from 'moment'
  export default {
    name: 'Index',
    components: { VabIcon },
    setup() {
      const store = useStore()
      return {
        username: computed(() => store.getters['user/username']),
      }
    },
    data() {
      return {
        radio: 1,
        charges: {
          1: {
            time: '7:00-10:00',
          },
          2: {
            time: '11:00-13:00',
          },
          3: {
            time: '17:00-19:00',
          },
        },
        book: {
          date: moment().format('YYYY-MM-DD'),
          time: '7:00-10:00',
        },
        booked: null,
      }
    },
    mounted() {
      this.getbooking()
    },
    methods: {
      moment,
      async getbooking() {
        let { data } = await getbooking(getAccessToken())
        this.booked = data
      },
      async unbooking() {
        let { data } = await unbooking(getAccessToken(), this.booked)
        message.warning(data)
        this.getbooking()
      },
      async usebooking() {
        let { data } = await usebooking(getAccessToken(), this.booked)
        message.success(data)
        this.getbooking()
      },
      async booking() {
        if (this.book.date) {
          let { data } = await booking(getAccessToken(), this.book)
          message.info(data)
          this.getbooking()
        } else {
          message.error('请选择日期')
        }
      },
      onChange: function (e) {
        this.book.time = this.charges[e.target.value].time
      },
      onDateChange: function (e) {
        this.book.date = e.format('YYYY-MM-DD')
      },
    },
  }
</script>
<style lang="less">
  .charge .ant-radio-group-large .ant-radio-button-wrapper {
    height: 53px;
    width: 155px;
    margin: 10px;
    font-size: 18px;
    line-height: 53px;
    text-align: center;
    color: #000;
  }
  .ant-radio-button-wrapper-checked:not(.ant-radio-button-wrapper-disabled) {
    background: url('~@/assets/charge_checked.jpg') no-repeat;
    background-size: 100% 100%;
  }
  .charge .ant-btn {
    width: 200px;
    height: 45px;
    border-radius: 99px;
  }
</style>
