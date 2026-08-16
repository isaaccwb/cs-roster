export function dv(val: any, suffix = ''): string {
  if (val === null || val === undefined || val === '') return '--'
  return `${val}${suffix}`
}
