import Image from 'next/image'
import Link from 'next/link'
import journalImage from '../static/img/journal.png'

const Navbar = () => {
    return (
        <nav className="flex justify-between items-center py-10 px-32 bg-white">
        <div className="icon-text-group">
        <Image src={journalImage} alt="Icon" height={60} />
          <span>SuperSaver</span>
        </div>
        <div className="button-group">
          <Link href="/spending_habits">Spending Habits </Link>
          <Link href="/total_savings">Total Savings </Link>
          <div className="savingsBtn">
            <Link href="/savings_journal" className="red-btnSavings">Savings Journal</Link>
          </div>
        </div>
      </nav>
    )
}

export default Navbar