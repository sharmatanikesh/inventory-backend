import { useEffect } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from "../ui/dialog"
import { Button } from "../ui/button"
import { Input } from "../ui/input"

const customerSchema = z.object({
  first_name: z.string().trim().min(1, "First name is required"),
  last_name: z.string().trim().min(1, "Last name is required"),
  email: z.string().trim().min(1, "Email address is required").email("Please enter a valid email address"),
  phone_number: z.string().optional().or(z.literal("")).refine(
    (val) => {
      if (!val) return true;
      const digits = val.replace(/\D/g, "");
      return digits.length === 10;
    },
    { message: "Phone number must contain exactly 10 digits" }
  )
})

export default function CustomerForm({ isOpen, onClose, onSubmit }) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors }
  } = useForm({
    resolver: zodResolver(customerSchema),
    defaultValues: {
      first_name: "",
      last_name: "",
      email: "",
      phone_number: ""
    }
  })

  useEffect(() => {
    if (isOpen) {
      reset({
        first_name: "",
        last_name: "",
        email: "",
        phone_number: ""
      })
    }
  }, [isOpen, reset])

  const handleFormSubmit = (data) => {
    onSubmit({
      first_name: data.first_name,
      last_name: data.last_name,
      email: data.email.toLowerCase(),
      phone_number: data.phone_number.trim() || null
    })
  }

  return (
    <Dialog open={isOpen} onOpenChange={(val) => !val && onClose()}>
      <DialogContent className="sm:max-w-[400px] border border-slate-100 bg-white">
        <DialogHeader>
          <DialogTitle className="text-lg font-bold text-slate-800">
            Register Customer
          </DialogTitle>
        </DialogHeader>

        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4 py-2">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                First Name
              </label>
              <Input
                {...register("first_name")}
                placeholder="e.g. John"
                className={`text-sm ${errors.first_name ? "border-rose-500 focus-visible:ring-rose-500" : ""}`}
              />
              {errors.first_name && (
                <p className="text-[10px] font-semibold text-rose-600 mt-0.5">
                  {errors.first_name.message}
                </p>
              )}
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
                Last Name
              </label>
              <Input
                {...register("last_name")}
                placeholder="e.g. Doe"
                className={`text-sm ${errors.last_name ? "border-rose-500 focus-visible:ring-rose-500" : ""}`}
              />
              {errors.last_name && (
                <p className="text-[10px] font-semibold text-rose-600 mt-0.5">
                  {errors.last_name.message}
                </p>
              )}
            </div>
          </div>

          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Email Address
            </label>
            <Input
              type="email"
              {...register("email")}
              placeholder="e.g. john.doe@example.com"
              className={`text-sm ${errors.email ? "border-rose-500 focus-visible:ring-rose-500" : ""}`}
            />
            {errors.email && (
              <p className="text-[10px] font-semibold text-rose-600 mt-0.5">
                {errors.email.message}
              </p>
            )}
          </div>

          <div className="space-y-1">
            <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Phone Number (Optional)
            </label>
            <Input
              type="tel"
              {...register("phone_number")}
              placeholder="e.g. 555-019-2834"
              className={`text-sm ${errors.phone_number ? "border-rose-500 focus-visible:ring-rose-500" : ""}`}
            />
            {errors.phone_number && (
              <p className="text-[10px] font-semibold text-rose-600 mt-0.5">
                {errors.phone_number.message}
              </p>
            )}
          </div>

          <DialogFooter className="pt-4 flex gap-2">
            <Button type="button" variant="outline" onClick={onClose} className="text-xs font-semibold">
              Cancel
            </Button>
            <Button type="submit" className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold shadow-md shadow-indigo-100">
              Register Customer
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}
