import { Card, CardContent, CardHeader, CardTitle } from "../ui/card"
import { Package, Users, ShoppingCart } from "lucide-react"

export default function StatsOverview({ totalProducts = 0, totalCustomers = 0, totalOrders = 0 }) {
  const cards = [
    {
      title: "Total Products",
      value: totalProducts,
      icon: Package,
      color: "text-indigo-600",
      bgColor: "bg-indigo-50",
      description: "Available items in inventory"
    },
    {
      title: "Total Customers",
      value: totalCustomers,
      icon: Users,
      color: "text-emerald-600",
      bgColor: "bg-emerald-50",
      description: "Registered client accounts"
    },
    {
      title: "Total Orders",
      value: totalOrders,
      icon: ShoppingCart,
      color: "text-amber-600",
      bgColor: "bg-amber-50",
      description: "Processed transactions"
    }
  ]

  return (
    <div className="grid gap-6 md:grid-cols-3">
      {cards.map((card) => {
        const Icon = card.icon
        return (
          <Card key={card.title} className="overflow-hidden border border-slate-100 bg-white hover:shadow-md transition-all duration-200">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-xs font-bold uppercase tracking-wider text-slate-400">
                {card.title}
              </CardTitle>
              <div className={`rounded-lg p-2.5 ${card.bgColor} shadow-sm`}>
                <Icon className={`h-5 w-5 ${card.color}`} />
              </div>
            </CardHeader>
            <CardContent className="pt-1">
              <div className="text-3xl font-extrabold tracking-tight text-slate-800">
                {card.value}
              </div>
              <p className="mt-1 text-xs text-slate-400 font-medium">
                {card.description}
              </p>
            </CardContent>
          </Card>
        )
      })}
    </div>
  )
}
