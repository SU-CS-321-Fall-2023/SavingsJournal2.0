import Image from 'next/image'
import './styles.css'
import coinsImage from './static/img/coins.jpg'
import moneyTreeImage from './static/img/moneytree2.jpg';
import savingsJarImage from './static/img/savingsjar.jpg';
import savingsWalletImage from './static/img/savingswallet.jpg';

export default function Home() {
  return (
    <>
    <div className="content">
      <Image
        src={moneyTreeImage}
        alt="Big Image"
        className="big-image"
        width={1000}
        height={1000}
      />
      <div>
        <h1>
          Changing <br />
          savings one <br />
          day at a time
        </h1>
        <p>
          Join now and get 50% off <br /> and the deal of a lifetime <br />
          right before your eyes
        </p>
        <div className="startBtn">
          <button className="red-btn">Start Now</button>
        </div>
      </div>
    </div>
    {/* Line Separator */}
    <hr />
    {/* Additional sections as described */}
    {/* ... */}
    <div className="content">
      <Image
        src={coinsImage}
        alt="Big Image"
        className="coins-image"
        width={1000}
        height={1000}
      />
      <div>
        <p className="coins-text">
          Savings such a hassle.
          <br /> Allow us to take it from
          <br /> here!
        </p>
      </div>
    </div>
    <div className="content">

      <Image
        src={savingsJarImage}
        alt="Big Image"
        className="jar-image"
        width={1000}
        height={1000}
      />
      <div>
        <p className="jar-text">
          With SuperSaver, you’ll
          <br /> be able to manage and
          <br /> keep track of the things
          <br /> you want in no time.
        </p>
      </div>
    </div>
    <div className="content">
            <Image
        src={savingsWalletImage}
        alt="Big Image"
        className="jar-image"
        width={1000}
        height={1000}
      />
      <div>
        <p className="wallet-text">
          Don’t lose focus on the
          <br /> things you want with
          <br />
          SuperSaver.
        </p>
      </div>
    </div>
  </>  
  )
}
