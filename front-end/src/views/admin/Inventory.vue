<template>
  <div>
    <a-table bordered :data-source="data" :columns="columns">
      <template #inventory="{ text, record }">
        <div class="editable-cell">
          <div
            v-if="editableData[record.key]"
            class="editable-cell-input-wrapper"
          >
            <a-input
              v-model:value="editableData[record.key].inventory"
              @pressEnter="save(record.key)"
            />
            <check-outlined
              class="editable-cell-icon-check"
              @click="save(record.key)"
            />
          </div>
          <div v-else class="editable-cell-text-wrapper">
            <a-row>
              <a-col :span="14">
                {{ text }}
              </a-col>
              <a-col :span="10">
                <edit-outlined
                  class="editable-cell-icon"
                  @click="edit(record.key)"
                />
              </a-col>
            </a-row>
          </div>
        </div>
      </template>
    </a-table>
  </div>
</template>
<script>
  import { getItems, updateInventory } from '@/api/table'
  import { CheckOutlined, EditOutlined } from '@ant-design/icons-vue'
  import { cloneDeep } from 'lodash-es'
  import { message } from 'ant-design-vue'
  export default {
    components: {
      CheckOutlined,
      EditOutlined,
    },
    data() {
      return {
        data: [],
        pagination: {
          showLessItems: true,
          showQuickJumper: true,
          showSizeChanger: true,
          pageSize: 10,
          current: 1,
        },
        query: {},
        editableData: {},
        editingKey: '',
        loading: false,
        columns: [
          {
            title: 'name',
            dataIndex: 'item_name',
            width: '25%',
            slots: {
              customRender: 'item_name',
            },
          },
          {
            title: 'type',
            dataIndex: 'item_type',
            width: '15%',
            slots: {
              customRender: 'item_type',
            },
          },
          {
            title: 'price',
            dataIndex: 'item_price',
            width: '10%',
            slots: {
              customRender: 'item_price',
            },
          },
          {
            title: 'inventory',
            dataIndex: 'inventory',
            width: '10%',
            slots: {
              customRender: 'inventory',
            },
          },
        ],
      }
    },
    mounted() {
      this.fetch()
    },
    methods: {
      handleTableChange(pagination) {
        const pager = { ...this.pagination }
        pager.current = pagination.current
        this.pagination = pager
        this.fetch()
      },
      edit(key) {
        let e = this.data.filter((item) => key === item.key)[0]
        this.editableData[key] = cloneDeep(e)
      },
      async save(key) {
        for (const k in this.editableData[key]) {
          if (Object.hasOwnProperty.call(this.editableData[key], k)) {
            const element = this.editableData[key][k]
            if (element == undefined || element == '' || element.length == 0) {
              message.error('字段不能为空')
              return
            }
          }
        }
        let e = this.data.filter((item) => key === item.key)[0]
        const { data } = await updateInventory(this.editableData[key])
        let i = this.data.indexOf(e)
        e.key = data + ''
        e.id = data
        this.data.splice(i, 1, this.editableData[key])
        delete this.editableData[key]
      },
      fetch() {
        this.loading = true
        getItems({
          pageSize: this.pagination.pageSize,
          current: this.pagination.current,
        }).then(({ data, total }) => {
          const pagination = { ...this.pagination }
          pagination.total = total
          this.loading = false
          this.data = data
          this.pagination = pagination
        })
      },
    },
  }
</script>
<style lang="less">
  .editable-cell {
    position: relative;
    .editable-cell-input-wrapper,
    .editable-cell-text-wrapper {
      padding-right: 24px;
    }

    .editable-cell-text-wrapper {
      padding: 5px 24px 5px 5px;
    }

    .editable-cell-icon,
    .editable-cell-icon-check {
      position: absolute;
      right: 0;
      width: 20px;
      cursor: pointer;
    }

    .editable-cell-icon {
      display: none;
    }

    .editable-cell-icon-check {
      line-height: 35px;
    }

    .editable-cell-icon:hover,
    .editable-cell-icon-check:hover {
      color: #108ee9;
    }
  }
  .editable-cell:hover .editable-cell-icon {
    display: inline-table;
  }
</style>
