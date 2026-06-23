import { cn } from "../../lib/utils"

export default function Skeleton({ className, ...props }) {
  return (
    <div
      className={cn("animate-pulse rounded-md bg-slate-200/80", className)}
      {...props}
    />
  )
}

export function TableSkeleton({ rows = 5, cols = 4 }) {
  return (
    <div className="w-full rounded-lg border border-slate-200/60 bg-white overflow-hidden shadow-sm">
      <div className="border-b border-slate-200 bg-slate-50/70 h-10 flex items-center px-4 gap-4">
        {Array.from({ length: cols }).map((_, i) => (
          <Skeleton key={i} className="h-4 flex-1" />
        ))}
      </div>
      <div className="divide-y divide-slate-100">
        {Array.from({ length: rows }).map((_, r) => (
          <div key={r} className="h-14 flex items-center px-4 gap-4">
            {Array.from({ length: cols }).map((_, c) => (
              <Skeleton key={c} className="h-4 flex-1" />
            ))}
          </div>
        ))}
      </div>
    </div>
  )
}

export function DashboardSkeleton() {
  return (
    <div className="space-y-8 animate-pulse">
      {/* Header breadcrumb skeleton */}
      <div className="flex justify-between items-center">
        <div className="space-y-1.5">
          <Skeleton className="h-3.5 w-24" />
          <Skeleton className="h-6 w-32" />
        </div>
        <Skeleton className="h-8 w-24 rounded-lg" />
      </div>

      {/* Stats Cards grid */}
      <div className="grid gap-5 sm:grid-cols-3">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="rounded-lg border border-slate-100 bg-white p-6 shadow-sm flex items-center gap-4">
            <Skeleton className="h-12 w-12 rounded-lg bg-slate-200" />
            <div className="space-y-2 flex-1">
              <Skeleton className="h-3 w-16" />
              <Skeleton className="h-6 w-24" />
            </div>
          </div>
        ))}
      </div>

      {/* Low Stock Alerts Table card */}
      <div className="rounded-lg border border-slate-100 bg-white p-6 shadow-sm space-y-4">
        <div className="space-y-2">
          <Skeleton className="h-4 w-32" />
          <Skeleton className="h-3 w-48" />
        </div>
        <div className="space-y-3 pt-2">
          <div className="h-9 border-b border-slate-100 flex items-center gap-4 px-2">
            <Skeleton className="h-3.5 w-16" />
            <Skeleton className="h-3.5 w-32" />
            <Skeleton className="h-3.5 w-12 ml-auto" />
            <Skeleton className="h-3.5 w-16 ml-12" />
          </div>
          {Array.from({ length: 4 }).map((_, i) => (
            <div key={i} className="h-12 border-b border-slate-50 flex items-center gap-4 px-2">
              <Skeleton className="h-3.5 w-20" />
              <Skeleton className="h-4 w-40" />
              <Skeleton className="h-4 w-8 ml-auto" />
              <Skeleton className="h-5 w-16 ml-12 rounded-full" />
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export function CreateOrderSkeleton() {
  return (
    <div className="space-y-6 animate-pulse">
      {/* Header and Back Button */}
      <div className="flex justify-between items-center">
        <div className="space-y-1.5">
          <Skeleton className="h-3.5 w-24" />
          <Skeleton className="h-6 w-36" />
        </div>
        <Skeleton className="h-8 w-28 rounded-lg" />
      </div>

      <div className="flex flex-col lg:flex-row gap-6">
        {/* Left Section: Order Items Builder */}
        <div className="flex-1 rounded-lg border border-slate-100 bg-white p-6 shadow-sm space-y-5">
          <div className="flex items-center justify-between border-b border-slate-50 pb-4 mb-5">
            <Skeleton className="h-4 w-24" />
            <Skeleton className="h-8 w-24 rounded-lg" />
          </div>

          <div className="space-y-4">
            {Array.from({ length: 2 }).map((_, idx) => (
              <div key={idx} className="flex flex-col sm:flex-row gap-3 border border-slate-100 rounded-lg p-4 bg-slate-50/30">
                <div className="flex-1 space-y-2">
                  <Skeleton className="h-3 w-16" />
                  <Skeleton className="h-10 w-full rounded-md" />
                </div>
                <div className="w-full sm:w-28 space-y-2">
                  <Skeleton className="h-3 w-12" />
                  <Skeleton className="h-10 w-full rounded-md" />
                </div>
                <div className="flex items-end justify-end sm:pt-5 sm:pl-2">
                  <Skeleton className="h-10 w-10 rounded-md" />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right Section: Customer & Total Panel */}
        <div className="w-full lg:w-96 space-y-6">
          <div className="rounded-lg border border-slate-100 bg-white p-6 shadow-sm space-y-4">
            <div className="space-y-2">
              <Skeleton className="h-3 w-20" />
              <Skeleton className="h-10 w-full rounded-md" />
            </div>
          </div>

          <div className="rounded-lg border border-slate-100 bg-white p-6 shadow-sm space-y-5">
            <div className="space-y-3">
              <div className="flex justify-between">
                <Skeleton className="h-3 w-20" />
                <Skeleton className="h-3 w-12" />
              </div>
              <div className="flex justify-between">
                <Skeleton className="h-3 w-24" />
                <Skeleton className="h-3 w-10" />
              </div>
            </div>
            <div className="flex items-center justify-between border-t border-slate-50 pt-4 mt-2">
              <Skeleton className="h-3.5 w-16" />
              <Skeleton className="h-6 w-20" />
            </div>
            <div className="pt-2 space-y-2">
              <Skeleton className="h-10 w-full rounded-lg" />
              <Skeleton className="h-10 w-full rounded-lg" />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
