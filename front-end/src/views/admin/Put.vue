<template>
  <div>
    <a-button
      class="editable-add-btn"
      @click="handleAdd"
      style="margin-bottom: 8px;"
      :disabled="Object.keys(editableData).length > 0"
    >
      新增
    </a-button>
    <a-table :columns="columns" :data-source="data" bordered>
      <template
        v-for="col in ['item_name', 'item_type', 'item_price']"
        #[col]="{ text, record }"
        :key="col"
      >
        <div>
          <a-input
            v-if="editableData[record.key]"
            v-model:value="editableData[record.key][col]"
            style="margin: -5px 0;"
          />
          <template v-else>
            {{ text }}
          </template>
        </div>
      </template>
      <template #operation="{ record }">
        <div class="editable-row-operations">
          <span v-if="editableData[record.key]">
            <a @click="save(record.key)">Save</a>
            &nbsp;
            <a-popconfirm title="Sure to cancel?" @confirm="cancel(record.key)">
              <a>Cancel</a>
            </a-popconfirm>
          </span>
          <span v-else>
            <a @click="edit(record.key)">Edit</a>
          </span>
          &nbsp;
          <span v-if="record.id !== undefined">
            <a @click="delItem(record.key)">Delete</a>
          </span>
        </div>
      </template>
    </a-table>
  </div>
</template>
<script>
  import { getItems, saveItem, delItem } from '@/api/table'
  import { cloneDeep } from 'lodash-es'
  import { message } from 'ant-design-vue'
  export default {
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
            title: 'operation',
            dataIndex: 'operation',
            slots: {
              customRender: 'operation',
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
      async delItem(key) {
        let e = this.data.filter((item) => key === item.key)[0]
        await delItem(e)
        let i = this.data.indexOf(e)
        this.data.splice(i, 1)
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
        const { data } = await saveItem(this.editableData[key])
        let i = this.data.indexOf(e)
        e.key = data + ''
        e.id = data
        this.data.splice(i, 1, this.editableData[key])
        delete this.editableData[key]
      },
      cancel(key) {
        delete this.editableData[key]
        if ((key + '').startsWith('temp')) {
          let e = this.data.filter((item) => key === item.key)[0]
          let i = this.data.indexOf(e)
          this.data.splice(i, 1)
        }
      },
      handleAdd() {
        let key = this.data.length + 1
        key = 'temp_' + key
        this.data.push({
          key: key,
          item_name: ``,
          item_type: ``,
          item_price: ``,
        })
        this.edit(key)
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
