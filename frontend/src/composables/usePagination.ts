import { reactive } from 'vue'

export function usePagination(defaultPageSize = 10) {
  const pagination = reactive({
    page: 1,
    page_size: defaultPageSize,
    total: 0
  })

  function reset() {
    pagination.page = 1
  }

  function setTotal(total: number) {
    pagination.total = total
  }

  return { pagination, reset, setTotal }
}
