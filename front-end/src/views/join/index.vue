<template>
  <div class="parent">
    <a-form
      class="child-half-top"
      style="width: 600px; margin: 0 auto"
      ref="formRef"
      name="custom-validation"
      :model="formState"
      :rules="rules"
      v-bind="layout"
      @finish="handleFinish"
      @validate="handleValidate"
      @finishFailed="handleFinishFailed"
    >
      <a-form-item has-feedback label="用户名" name="user">
        <a-input v-model:value="formState.user" autocomplete="off" />
      </a-form-item>
      <a-form-item has-feedback label="密码" name="pass">
        <a-input
          v-model:value="formState.pass"
          type="password"
          autocomplete="off"
        />
      </a-form-item>
      <a-form-item has-feedback label="确认密码" name="checkPass">
        <a-input
          v-model:value="formState.checkPass"
          type="password"
          autocomplete="off"
        />
      </a-form-item>
      <a-form-item :wrapper-col="{ span: 14, offset: 4 }">
        <a-button type="primary" html-type="submit">Submit</a-button>
        <a-button style="margin-left: 10px" @click="resetForm">Reset</a-button>
      </a-form-item>
    </a-form>
  </div>
</template>
<script>
  import { defineComponent, reactive, ref, createVNode } from 'vue'
  import { ExclamationCircleOutlined } from '@ant-design/icons-vue'
  import { hasUser, register } from '@/api/user'
  import { useStore } from 'vuex'
  import { useRouter } from 'vue-router'
  import { Modal } from 'ant-design-vue'
  export default defineComponent({
    setup() {
      const formRef = ref()
      const formState = reactive({
        user: undefined,
        pass: '',
        checkPass: '',
      })

      let checkUser = async (_rule, value) => {
        if (!value) {
          return Promise.reject('Please input the user')
        }
        let { data } = await hasUser(value)
        if (data > 0) {
          return Promise.reject('The user name already exists')
        }
        return Promise.resolve()
      }

      let validatePass = async (_rule, value) => {
        if (value === '') {
          return Promise.reject('Please input the password')
        } else {
          if (formState.checkPass !== '') {
            formRef.value.validateFields('checkPass')
          }
          return Promise.resolve()
        }
      }

      let validatePass2 = async (_rule, value) => {
        if (value === '') {
          return Promise.reject('Please input the password again')
        } else if (value !== formState.pass) {
          return Promise.reject("Two inputs don't match!")
        } else {
          return Promise.resolve()
        }
      }

      const rules = {
        pass: [
          {
            required: true,
            validator: validatePass,
            trigger: 'change',
          },
        ],
        checkPass: [
          {
            validator: validatePass2,
            trigger: 'change',
          },
        ],
        user: [
          {
            required: true,
            validator: checkUser,
            trigger: 'change',
          },
        ],
      }
      const layout = {
        labelCol: {
          span: 4,
        },
        wrapperCol: {
          span: 20,
        },
      }

      const store = useStore()
      const router = useRouter()

      const logout = async () => {
        await store.dispatch('user/logout')
        await store.dispatch('tagsBar/delAllVisitedRoutes')
        router.push('/login')
      }

      const handleFinish = async (values) => {
        console.log(values, formState)
        let { data } = await register(values)
        console.log(data)
        Modal.confirm({
          content: '注册成功,现在登陆?',
          icon: createVNode(ExclamationCircleOutlined),
          onOk() {
            logout()
          },
          cancelText: 'No',
          okText: 'Yes',
          onCancel() {},
        })
      }

      const handleFinishFailed = (errors) => {
        console.log(errors)
      }

      const resetForm = () => {
        formRef.value.resetFields()
      }

      const handleValidate = (...args) => {
        console.log(args)
      }

      return {
        formState,
        formRef,
        rules,
        layout,
        handleFinishFailed,
        handleFinish,
        resetForm,
        handleValidate,
      }
    },
  })
</script>
