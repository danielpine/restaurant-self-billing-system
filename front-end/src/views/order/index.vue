<template>
  <a-table
    :columns="columns"
    :row-key="(record) => record.key"
    :data-source="data"
    :pagination="pagination"
    :loading="loading"
    @change="handleTableChange"
  ></a-table>
</template>
<script>
  import { getList } from '@/api/table'

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
        loading: false,
        columns:[],
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
      fetch() {
        this.loading = true
        getList({
          pageSize: this.pagination.pageSize,
          current: this.pagination.current,
        }).then(({ data, total,columns }) => {
          const pagination = { ...this.pagination }
          pagination.total = total
          this.loading = false
          this.data = data
          this.columns = columns
          this.pagination = pagination
        })
      },
    },
  }
</script>
