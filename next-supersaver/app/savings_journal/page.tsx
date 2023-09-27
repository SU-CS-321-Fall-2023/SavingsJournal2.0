
export default function SavingsJournal() {
    return (
        <div className="container">
  <div className="mx-auto text-center flex flex-col items-center">
    {/* Heading */}
    <div className="text-4xl font-bold text-red-400">Savings Journal</div>
    {/* Buttons Group */}
    <div className="space-x-2 mt-4">
      <button
        type="button"
        className="text-black hover:bg-red-200 text-md px-5 py-2.5 rounded-2xl transition ease-in-out delay-100"
      >
        Done
      </button>
      <button
        type="button"
        className="text-black hover:bg-red-200 text-sm px-5 py-2.5 rounded-2xl transition ease-in-out delay-100"
      >
        Doing
      </button>
      <button
        type="button"
        className="text-black hover:bg-red-200 text-sm px-5 py-2.5 rounded-2xl transition ease-in-out delay-100"
      >
        Todo
      </button>
    </div>
  </div>
</div>
    )
}